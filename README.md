# igqloo

A small tool for interacting with GQL APIs

Arguments, mutations, aliases are all supported. Other features, such as
fragments, are left unsupported with the opinion that, when a query becomes
large enough to warrant them, you might be best feeding in a file containing
your query.

```bash
igqloo <graphql_uri> customer(name:"gerhalt@gmail.com").id,firstName,lastName
```

Under the surface, generates a GraphQL query that looks like:

```json
query {
    customer(name:"gerhalt@gmail.com") {
        id, firstName, lastName
    }
}
```

Queries are made simple using three key concepts:

1. Dot-notation, with `.` indicating the beginning of a nested query level
2. A comma `,` indicates a field on the same level as the prior field
3. Parenthesis `()` for filters and "quoting" aliases
