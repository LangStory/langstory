export default interface ApiCollectionResponse<T> {
    items: Array<T>
    data: T
    page: number
    pages: number
}
