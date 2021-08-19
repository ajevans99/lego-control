import graphene
import systems.schema


class Query(systems.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(systems.schema.Mutation, graphene.ObjectType):
    pass


class Subscription(systems.schema.Subscription, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
