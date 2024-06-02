from typing import List, Optional, Tuple, Type, TYPE_CHECKING, Union
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.orm.properties import ColumnProperty
from shlex import split
from dateutil import parser

from app.logger import get_logger
from app.controllers.mixins.database_mixin import DatabaseMixin

if TYPE_CHECKING:
    from app.models.base import Base
    from app.models.user import User
    from app.schemas.user_schemas import ScopedUser
    from sqlalchemy.sql.selectable import Select
    from sqlalchemy import Column
    from app.schemas.collection_schemas import CollectionRequest, CollectionResponse
    from sqlalchemy.orm import Session

logger = get_logger(__name__)


class CollectionMixin(DatabaseMixin):
    """supports listing, pagination, and searching of object collections"""

    def __init__(self, db_session: "Session", ModelClass: Type["Base"]):
        super().__init__(db_session)
        self.ModelClass = ModelClass

    def get_collection(
        self, request: "CollectionRequest", select_: Optional["Select"] = None
    ) -> "CollectionResponse":
        """shorthand for get_paginated_collection"""
        # cannot infer type of ScopedUser at this time
        return self.get_paginated_collection(
            self.ModelClass,
            actor=request.actor,
            select_=select_,
            **request.model_dump(exclude_none=True, exclude=["actor"]),
        )

    def get_paginated_collection(
        self,
        ModelClass: Type["Base"],
        actor: Union["ScopedUser", "User"],
        page: int,
        per_page: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[str] = None,
        power_filter: Optional[str] = None,
        select_: Optional["Select"] = None,
    ) -> Tuple[List[Type["Base"]], int]:
        """DEPRECATED: use get_collection, which will eventually replace this method
        select_: a pre-built select query to use instead of building a new one
        """
        # defaults post-none, as upstream may set these to None
        page = max(
            (
                page or 1,
                1,
            )
        )
        per_page = per_page or 25
        order_dir = order_dir or "asc"
        order_by = order_by or getattr(ModelClass, "__order_by_default__")

        orderable = self._get_orderable(ModelClass, order_by, order_dir)
        query = select_ or select(ModelClass)
        if hasattr(ModelClass, "deleted"):
            query = query.where(ModelClass.deleted == False)
        query = ModelClass.apply_access_predicate(query, actor, "read")

        if power_filter:
            query = self.apply_power_filter(ModelClass, query, power_filter)

        page_count = (self._get_total_count(query) + per_page - 1) // per_page

        final_query = (
            query.order_by(orderable).limit(per_page).offset((page - 1) * per_page)
        )
        instances = self._get_results(final_query)

        return instances, page_count

    def apply_power_filter(
        self, model: Type["Base"], statement: "Select", power_filter: str
    ) -> "Select":
        """Apply a power query filter to a sqlalchemy query.
        Args:
            - model: the base model that is being queried
            - statement: the sqlalchemy query object
            - power_filter: a power query string
        Returns:
            - a sqlalchemy query object with filters applied
        Note: If ANY of the filters are "bad" (not valid for the object) scopes 'where 1=0' to kill the query
        """
        # break out the filter elements
        filter_elements = split(power_filter)
        bare_elements = []
        groupings = []

        # anything inside a grouping is searched with "and"
        grouping_markers = self._get_grouping_markers(filter_elements)
        if len(grouping_markers) % 2 != 0:
            logger.error("unbalanced parenthesis in query: %s", power_filter)
            return statement.where(False)
        marker_pairs = self._get_marker_pairs(grouping_markers)

        bare_elements, groupings = self._assemble_elements(
            filter_elements, marker_pairs
        )
        logger.debug("groupings: %s", groupings)
        logger.debug("bare_elements: %s", bare_elements)

        statement_predicates = []
        statement_predicates.append(
            self._get_groupings_predicates(model, statement, groupings)
        )
        statement_predicates.append(
            self._get_bare_predicates(model, statement, bare_elements)
        )
        statement = statement.where(or_(*statement_predicates))
        logger.debug("final arguments: %s", statement.compile().params)
        logger.debug("final statement: %s", statement)
        return statement

    def build_predicate(
        self, ModelClass: Type["Base"], statement: "Select", element: str
    ) -> Tuple["Select", List]:
        """constructs a filter predicate for a given element, that can be assembled into a select.where() clause
        Args:
            - model: the base model that is being queried
            - statement: the sqlalchemy select query object
            - element: a single element from a power query string
        Returns:
            - The modified select (with needed joins etc) and list of sqlalchemy filter predicates to be assembed into a WHERE clause
        """
        try:
            attribute, operator, value = self._get_core_components(element)
        except ValueError as e:
            return statement.where(False), []

        value = self._set_wildcards(value)
        try:
            value = self._cast_timestamps(attribute, value)
        except parser._parser.ParserError:
            return statement.where(False), []

        if self._attempted_to_search_secrets(attribute):
            return statement.where(False), []

        predicates = []
        col = getattr(ModelClass, attribute, None)
        if not col:
            logger.error("bad filter attribute: %s", attribute)
            return statement.where(False), []

        if self._column_is_native_to_model(col):
            modifier = getattr(col, operator)(value)
            predicates.append(modifier)
            return statement, predicates
        try:
            target_class = aliased(col.property.mapper.class_)
            statement = self._apply_related_object_predicate(
                target_class, attribute, ModelClass, statement
            )
            modifier = target_class.related_lookup(value)
            predicates.append(modifier)
            return statement, predicates
        except (ValueError, AttributeError) as e:
            logger.error("bad filter attribute: %s : %s", attribute, e)
            return statement.where(False), []

    # private methods

    def _get_results(self, query: "Select") -> List[Type["Base"]]:
        cursor = self.db_session.execute(query)

        return cursor.scalars().unique().all()

    def _get_total_count(self, query: "Select") -> int:
        return self.db_session.scalar(select(func.count()).select_from(query))

    def _get_orderable(
        self, ModelClass: Type["Base"], order_by: str, dir: str
    ) -> "Column":
        """Get the orderable column for a model class.
        Args:
            - ModelClass: the model class to get the orderable column from
            - order_by: the column name to order by
            - dir: the direction to order by
        Returns:
            - the orderable column
        """
        orderable = getattr(ModelClass, order_by)
        if orderable is None:
            orderable = getattr(ModelClass, "__order_by_default__", "created_at")
        if dir.lower() == "desc":
            orderable = orderable.desc()
        return orderable

    def _get_grouping_markers(self, filter_elements: List[str]):
        grouping_markers = []
        for index, element in enumerate(filter_elements):
            if element.startswith("("):
                filter_elements[index] = element[1:]
                grouping_markers.append(index)
            if element.endswith(")"):
                filter_elements[index] = element[:-1]
                grouping_markers.append(index)
        return grouping_markers

    def _get_marker_pairs(self, grouping_markers: List[int]):
        marker_pairs = list(zip(grouping_markers[::2], grouping_markers[1::2]))
        logger.debug("marker_pairs: %s", marker_pairs)
        return marker_pairs

    def _assemble_elements(
        self, filter_elements: List, marker_pairs: List[str]
    ) -> Tuple[List[str], List[str]]:
        """builds the bare elements and groupings from a list of filter elements"""
        bare_elements = []
        groupings = []
        for index, pair in enumerate(marker_pairs):
            start, end = pair
            if not groupings and start > 0:
                bare_elements.append(filter_elements[:start])
            groupings.append(filter_elements[start : end + 1])
            if (index < len(marker_pairs) - 1) and marker_pairs[index + 1][0] - end > 1:
                bare_elements.append(
                    filter_elements[end + 1 : marker_pairs[index + 1][0]]
                )
            if index == len(marker_pairs) - 1:
                bare_elements.append(filter_elements[end + 1 :])
        if not groupings:
            bare_elements.append(filter_elements)
        return bare_elements, groupings

    def _get_groupings_predicates(
        self, ModelClass: Type["Base"], statement: "Select", groupings: List[str]
    ) -> "Select":
        for grouping in groupings:
            grouping_predicates = []
            for element in [e for e in grouping if e]:
                logger.debug("building grouping predicate: %s", element)
                statement, predicates = self.build_predicate(
                    ModelClass, statement, element
                )
                grouping_predicates.extend(predicates)
            if not predicates:
                continue
            return and_(*grouping_predicates)

    def _get_bare_predicates(
        self, ModelClass: Type["Base"], statement: "Select", bare_elements: List[str]
    ) -> "Select":
        for bare_group in bare_elements:
            bare_group_predicates = []
            for element in [e for e in bare_group if e]:
                logger.debug("building bare predicate: %s", element)
                statement, predicates = self.build_predicate(
                    ModelClass, statement, element
                )
                bare_group_predicates.extend(predicates)
                if not predicates:
                    continue
        return and_(*bare_group_predicates)

    def _attempted_to_search_secrets(self, attribute: str) -> bool:
        """Don't let people search by secrets"""
        return attribute in (
            "password",
            "token_hash",
        )

    def _get_core_components(cls, element: str) -> Tuple[str, str, str]:
        """parses the element and returns a tuple of attribute, operator, and value"""
        ops = {
            "==": "ilike",
            "!=": "__ne__",
            "<": "__lt__",
            "<=": "__le__",
            ">": "__gt__",
            ">=": "__ge__",
        }
        if ":" not in element:
            message = f"bad filter element, no colon separator: {element}"
            logger.error(message)
            raise ValueError(message)
        attribute, value = element.split(":", 1)
        operator = "ilike"
        for operator_symbol in (
            "<=",
            ">=",
            "!=",
            "<",
            ">",
        ):
            if value.startswith(operator_symbol):
                value = value[len(operator_symbol) :]
                operator = ops[operator_symbol]
                return attribute, operator, value
        raise ValueError(f"bad filter element, no recognized operator: {element}")

    def _set_wildcards(cls, value: str) -> str:
        """use a wildcard character that humans can understand, remove string wrappers"""
        return value.replace("*", "%").replace("'", "").replace('"', "").strip()

    def _cast_timestamps(cls, attribute: str, value: str) -> str:
        """this is not the best solution for typing but works in the moment"""
        if attribute.endswith("_at"):
            value = parser.parse(value).date()

    def _column_is_native_to_model(cls, col) -> bool:
        return isinstance(col.property, ColumnProperty)

    def _apply_related_object_predicate(
        cls,
        target_class,
        attribute: str,
        ModelClass: Type["Base"],
        statement: "Select",
    ) -> "Select":
        source_id = getattr(ModelClass, f"{attribute}_id", None)
        if not source_id:
            message = f"There is no standard id pattern for accessing {attribute} on {ModelClass}. Please create a standard id pattern."
            logger.error(message)
            raise ValueError(message)
        return statement.join(target_class, onclause=target_class._id == source_id)
