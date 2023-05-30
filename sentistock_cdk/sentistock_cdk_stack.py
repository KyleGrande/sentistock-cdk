from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_apigatewayv2 as apigw2
)
from constructs import Construct

class SentistockCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Cognito
        user_pool = cognito.UserPool(self, "MyUserPool",
            user_pool_name="SentiStockUserPool",
            self_sign_up_enabled=True,
            sign_in_case_sensitive=False,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes={
                "given_name": cognito.StandardAttribute(required=True),
            },
            password_policy=cognito.PasswordPolicy(
                temp_password_validity=Duration.days(7),
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
            ),
            mfa=cognito.Mfa.OFF,
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY 
            )

        # Cognito App Client
        app_client = cognito.UserPoolClient(self, "MyUserPoolClient",
            user_pool=user_pool,
            user_pool_client_name="SentiStockClient",
            auth_flows=cognito.AuthFlow(
                user_password=True,
                custom=True
            ),
            access_token_validity=Duration.minutes(60),
            id_token_validity=Duration.minutes(60),
            refresh_token_validity=Duration.days(30),
            prevent_user_existence_errors=True,
            enable_token_revocation=True,
        )


        # DynamoDB Tables
        # StockQuotes Table
        stock_quotes_table = dynamodb.Table(
            self, "StockQuotes",
            table_name="StockQuotes",
            partition_key=dynamodb.Attribute(
                name="ticker",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=False,
            removal_policy=RemovalPolicy.DESTROY  # Set removal_policy
        )

        # UserStocks Table
        user_stocks_table = dynamodb.Table(
            self, "UserStocks",
            table_name="UserStocks",
            partition_key=dynamodb.Attribute(
                name="user_cognito_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=False,
            removal_policy=RemovalPolicy.DESTROY 
        )

        # Lambda Functions
        get_stock_lambda = _lambda.Function(
            self, "getStock",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/getStock/"),
            handler="lambda_handler.lambda_handler",
        )

        add_user_stocks_lambda = _lambda.Function(
            self, "addUserStocks",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/addUserStocks/"),
            handler="lambda_handler.lambda_handler",
        )

        target_sentiment_analysis_lambda = _lambda.Function(
            self, "targetSentimentAnalysis",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/targetSentimentAnalysis/"),
            handler="lambda_handler.lambda_handler",
        )

        get_top_by_index_lambda = _lambda.Function(
            self, "getTopByIndex",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/getTopByIndex/"),
            handler="lambda_handler.lambda_handler",
        )

        sentiment_analysis_lambda = _lambda.Function(
            self, "sentimentAnalysis",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/sentimentAnalysis/"),
            handler="lambda_handler.lambda_handler",
        )

        get_user_stocks_lambda = _lambda.Function(
            self, "getUserStocks",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/getUserStocks/"),
            handler="lambda_handler.lambda_handler",
        )

        remove_user_stock_lambda = _lambda.Function(
            self, "removeUserStock",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/removeUserStock/"),
            handler="lambda_handler.lambda_handler",
        )

        get_top_stocks_lambda = _lambda.Function(
            self, "getTopStocks",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/getTopStocks/"),
            handler="lambda_handler.lambda_handler",
        )

        update_top_by_index_lambda = _lambda.Function(
            self, "updateTopByIndex",
            runtime=_lambda.Runtime.PYTHON_3_10,
            code=_lambda.Code.from_asset("lambdas/updateTopByIndex/"),
            handler="lambda_handler.lambda_handler",
        )

        # API Gateway
        api = apigw.RestApi(self, "SentiStockApi",
            rest_api_name="SentiStockApi",
            description="API for SentiStock application",
        )

        # API Gateway Resources and Lambda Integrations
        get_stock_resource = api.root.add_resource("getstock")
        get_stock_integration = apigw.LambdaIntegration(get_stock_lambda, proxy=True)
        get_stock_resource.add_method("GET", get_stock_integration)

        add_user_stocks_resource = api.root.add_resource("adduserstock")
        add_user_stocks_integration = apigw.LambdaIntegration(add_user_stocks_lambda, proxy=True)
        add_user_stocks_resource.add_method("POST", add_user_stocks_integration)

        target_sentiment_analysis_resource = api.root.add_resource("gettargetsentiment")
        target_sentiment_analysis_integration = apigw.LambdaIntegration(target_sentiment_analysis_lambda, proxy=True)
        target_sentiment_analysis_resource.add_method("POST", target_sentiment_analysis_integration)

        get_top_by_index_resource = api.root.add_resource("gettopbyindex")
        get_top_by_index_integration = apigw.LambdaIntegration(get_top_by_index_lambda, proxy=True)
        get_top_by_index_resource.add_method("GET", get_top_by_index_integration)

        sentiment_analysis_resource = api.root.add_resource("getsentiment")
        sentiment_analysis_integration = apigw.LambdaIntegration(sentiment_analysis_lambda, proxy=True)
        sentiment_analysis_resource.add_method("POST", sentiment_analysis_integration)

        get_user_stocks_resource = api.root.add_resource("getuserstocks")
        get_user_stocks_integration = apigw.LambdaIntegration(get_user_stocks_lambda, proxy=True)
        get_user_stocks_resource.add_method("GET", get_user_stocks_integration)

        remove_user_stock_resource = api.root.add_resource("removeuserstock")
        remove_user_stock_integration = apigw.LambdaIntegration(remove_user_stock_lambda, proxy=True)
        remove_user_stock_resource.add_method("POST", remove_user_stock_integration)

        get_top_stocks_resource = api.root.add_resource("gettopstocks")
        get_top_stocks_integration = apigw.LambdaIntegration(get_top_stocks_lambda, proxy=True)
        get_top_stocks_resource.add_method("GET", get_top_stocks_integration)

        update_top_by_index_resource = api.root.add_resource("updatetopbyindex")
        update_top_by_index_integration = apigw.LambdaIntegration(update_top_by_index_lambda, proxy=True)
        update_top_by_index_resource.add_method("POST", update_top_by_index_integration)

        # Add OPTIONS method for CORS to all endpoints
        for resource in [
            get_stock_resource,
            add_user_stocks_resource,
            target_sentiment_analysis_resource,
            get_top_by_index_resource,
            sentiment_analysis_resource,
            get_user_stocks_resource,
            remove_user_stock_resource,
            get_top_stocks_resource,
            update_top_by_index_resource,
        ]:
            resource.add_method("OPTIONS", apigw.MockIntegration(
                integration_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'",
                        'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,GET,PUT,POST,DELETE'"
                    },
                }],
                passthrough_behavior=apigw.PassthroughBehavior.NEVER,
                request_templates={
                    "application/json": '{"statusCode": 200}'
                }
            ),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Methods': True,
                    'method.response.header.Access-Control-Allow-Origin': True,
                }
            }]
        )
