## Auth flow

The goal here is simplicity around a conventional path at the expense of less conventional paths.

This is the multi-tenant simple happy path we want to support as low-friction as possible:
1. Users have and utilize a work email domain (ie `dave@somecompany.com`).
2. Organizations are the work domain email (so `somecompany.com` is Dave's organization).
3. Only one organization should exist for any domain.
4. Everyone with that email domain should have at least read access to that organization (so `susan@somecompany.com` automatically belongs to the `somecompany.com` organization and can read projects in the `somecompany.com` organization).

For generic emails (@gmail etc)
1. user must select or create an organization
2. organization can be any name and avatar

Alternatively, users can self host a single tenant instance by setting the `LANGSTORY_SINGLE_TENANT` environment variable to True.
In that case:
1. Only one organization will be created.
2. Any new user from any email address will be given access to the organization.
3. To stop new user sign-ups, set the `LANGSTORY_ALLOW_NEW_USERS` environment variable to False.

If `LANGSTORY_VALIDATE_USER_EMAIL` then users will need to click an emailed validation link first before logging in.

Flow:
1. logs in/creates user - no org set in jwt
2. lands on select orgs page
  - all orgs granted to user show
  - (when user was created IF unique domain email, org was created for it OR user granted access if domain existed)
  - create new org is always an option
3. select org rebuilds jwt

! will need a way to add people to an org - probably just by email
- don't bother with a flow, just add them to it
