import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation  # absolute import

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=True)  # include mutation here!


'''import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

    # Optional: You can also define resolvers here if needed
    def resolve_hello(root, info):
        return "Hello, GraphQL!"

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
'''