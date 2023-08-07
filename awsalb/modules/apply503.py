import json
import boto3

def print_listener_rules(rules):
    print("Listener Rules:")
    for rule in rules:
        print(f"Rule ARN: {rule['RuleArn']}")
        print(f"Priority: {rule['Priority']}")
        print(f"Conditions: {rule['Conditions']}")
        print("Actions: {rule['Actions']}")
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

    # Find Rule with the specified condition
    rule_condition_found = False
    rule_condition_index = -1
    for index, rule in enumerate(rules):
        conditions = rule.get("Conditions", [])
        for condition in conditions:
            if "SourceIpConfig" in condition and condition["SourceIpConfig"]["Values"] == ["10.0.0.1/32"]:
                rule_condition_found = True
                rule_condition_index = index
                break
        if rule_condition_found:
            break

    if rule_condition_found:
        try:
            # Get the ARNs of Rule 1 and Rule with the specified condition
            rule_arn_1 = rules[0]["RuleArn"]
            rule_arn_condition = rules[rule_condition_index]["RuleArn"]

            # Switch rule priorities (Rule 1 becomes Rule with the specified condition, and Rule with the specified condition becomes Rule 1)
            elbv2_client.set_rule_priorities(
                RulePriorities=[
                    {"RuleArn": rule_arn_1, "Priority": int(rules[rule_condition_index]["Priority"])},
                    {"RuleArn": rule_arn_condition, "Priority": 1}
                ]
            )

            print("Rule priorities have been updated successfully.")
        except Exception as e:
            print(f"Error occurred while updating rule priorities: {e}")
    else:
        print("Rule with the specified condition not found.")

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
            send_sns_message(my_sns_topic_arn, "Applied 503 rule as Priority 1")
        except:
            # If an error occurs during the process, it means the rule priorities were not updated.
            send_sns_message(my_sns_topic_arn, "Failed to apply 503 rule as Priority 1")
    else:
        print(f"The SNS topic '{my_sns_topic_name}' was not found.")

    return {
        'statusCode': 200,
        'body': json.dumps('Rule priorities have been checked and updated if needed.')
    }
  