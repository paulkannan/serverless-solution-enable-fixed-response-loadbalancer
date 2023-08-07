import json
import boto3

def print_listener_rules(rules):
    print("Listener Rules:")
    for rule in rules:
        print(f"Rule ARN: {rule['RuleArn']}")
        print(f"Priority: {rule['Priority']}")
        print(f"Conditions: {rule['Conditions']}")
        print(f"Actions: {rule['Actions']}")
        print("-------------")

def check_and_switch_rule_priorities():
    # Create a Boto3 client for Elastic Load Balancing (ELBv2) using the default region of the Lambda function
    elbv2_client = boto3.client("elbv2", region_name=boto3.Session().region_name)

    # Get the ARN of your Application Load Balancer (ALB)
    response = elbv2_client.describe_load_balancers()
    alb_arn = response["LoadBalancers"][0]["LoadBalancerArn"]

    # Get the listener ARN of your ALB
    response = elbv2_client.describe_listeners(LoadBalancerArn=alb_arn)
    listener_arn = response["Listeners"][0]["ListenerArn"]

    # Get the listener rule ARNs associated with your ALB's listener
    response = elbv2_client.describe_rules(ListenerArn=listener_arn)
    rules = response["Rules"]

    # Print all listener rules and their conditions
    print_listener_rules(rules)

    # Find Rule with 'SourceIpConfig': {'Values': ['10.0.0.1/32']} in Priority 1
    rule_1_found = None
    for rule in rules:
        conditions = rule.get("Conditions", [])
        if any(condition.get("SourceIpConfig", {}).get("Values") == ['10.0.0.1/32'] for condition in conditions):
            if rule["Priority"] == "1":
                rule_1_found = rule
                break

    if rule_1_found:
        try:
            # Find Rule in Priority 3
            rule_3_found = None
            for rule in rules:
                if rule["Priority"] == "3":
                    rule_3_found = rule
                    break

            # Switch rule priorities (Rule 1 becomes Rule 3, and Rule in Priority 3 becomes Rule 1)
            elbv2_client.set_rule_priorities(
                RulePriorities=[
                    {"RuleArn": rule_1_found["RuleArn"], "Priority": int(rule_3_found["Priority"])},
                    {"RuleArn": rule_3_found["RuleArn"], "Priority": int(rule_1_found["Priority"])}
                ]
            )

            print("Rule priorities have been updated successfully.")
        except Exception as e:
            print(f"Error occurred while updating rule priorities: {e}")
    else:
        print("Rule with 'SourceIpConfig': {'Values': ['10.0.0.1/32']} in Priority 1 not found.")

def get_sns_topic_arn(topic_name):
    sns_client = boto3.client("sns")
    response = sns_client.list_topics()
    topics = response["Topics"]
    for topic in topics:
        if topic_name in topic["TopicArn"]:
            return topic["TopicArn"]
    return None

def send_sns_message(topic_arn, message):
    sns_client = boto3.client("sns")
    sns_client.publish(TopicArn=topic_arn, Message=message)

def lambda_handler(event, context):
    # Call the check_and_switch_rule_priorities function
    check_and_switch_rule_priorities()

    # Get the SNS topic ARN programmatically
    my_sns_topic_name = "MySNSTopic"
    my_sns_topic_arn = get_sns_topic_arn(my_sns_topic_name)

    if my_sns_topic_arn:
        try:
            # Assuming the function does not throw an error, if it reaches here, it means the rule priorities have been updated successfully.
            send_sns_message(my_sns_topic_arn, "Reverted 503 rule")
        except:
            # If an error occurs during the process, it means the rule priorities were not updated.
            send_sns_message(my_sns_topic_arn, "Failed to revert 503 rule")
    else:
        print(f"The SNS topic '{my_sns_topic_name}' was not found.")

    return {
        'statusCode': 200,
        'body': json.dumps('Rule priorities have been checked and updated if needed.')
    }
