# Serverless Solution enable fixed response in Loadbalancer
Serverless solution to enable maintenance status in AWS LoadBalancers


![awsalb](https://github.com/paulkannan/serverless-solution-enable-fixed-response-loadbalancer/assets/46925641/345d319b-6e02-4edc-a531-0d27a26e418f)


Managing maintenance windows for On-premises and AWS workloads, especially across multiple regions, can be a complex task for organizations. To address this challenge, we present a serverless solution that seamlessly implements static response mechanisms at the Application Load Balancer (ALB) level deployed in various regions. This approach offers a straightforward and cost-effective way to notify end users during maintenance periods without relying on additional AWS resources like static websites or Lambda functions.

With this serverless architecture, organizations can efficiently display customized maintenance messages to users, simplifying the management of maintenance windows across regions. The solution leverages AWS Lambda functions and ALBs in different regions, providing the flexibility and scalability needed to handle varying user traffic during maintenance activities.

Compared to traditional approaches that involve hosting static websites in S3 or deploying custom Lambda functions, this solution significantly reduces resource overhead and operational complexity. By eliminating the need for additional infrastructure, it streamlines the process of notifying users and reduces overall costs. Monitoring and alerting mechanisms further ensure smooth execution and immediate response to any potential issues during maintenance periods.

**Advantages of this approach:**

**Simplicity and Cost-Effectiveness:** Implementing a static response at the ALB level requires minimal configuration and avoids the overhead of setting up and maintaining additional AWS resources. This can lead to cost savings for organizations, especially for small-scale or occasional maintenance requirements.

**Centralized Management:** Managing the maintenance response directly at the ALB allows for centralized control over the response content. Any changes or updates to the maintenance message can be made directly within the Terraform code, ensuring consistency across all instances served by the ALB.

**Fast Response:** The static response is delivered at the load balancer level, enabling quick responses to user requests during maintenance windows. There's no need to wait for Lambda functions or website resources to spin up, reducing latency for users.

**Load Balancer Flexibility:** The use of ALB's listener rules provides flexibility to define different maintenance scenarios based on various conditions like user-agent, referrer, or source IP address. This allows organizations to target specific user groups or regions with different maintenance messages if required.

**No External Dependencies:** Unlike a static website hosted in S3, this solution does not have any external dependencies. The ALB can serve the maintenance response directly without relying on external services or network calls.

**To Deploy the code using Terraform:**

**Clone the Repository:** Start by cloning the GitHub repository to your local machine. Use the git clone command to clone the repository: **git clone**

**Navigate to the Repository:** Change into the cloned repository directory: **cd useast1, cd useast2**

**Review the Terraform Code: ** Explore the contents of the repository and locate the Terraform code files (e.g., .tf files) that define the infrastructure.

**Install Terraform:** Ensure that Terraform is installed on your local machine. You can download Terraform from the official website (https://www.terraform.io/downloads.html) and follow the installation instructions for your operating system.

**Initialize the Terraform Configuration:** Run **terraform init** in the repository directory to initialize the Terraform configuration. This command downloads the necessary provider plugins and sets up the working directory.Review Variables: Check if there are any variables defined in the Terraform code or provided through variable files (*.tfvars files). Modify the values of the variables as required.

**Plan the Infrastructure Changes:** Run **terraform plan** to preview the infrastructure changes that Terraform will make. This step provides an overview of the resources that will be created, modified, or destroyed.

**Apply the Infrastructure Changes:** If you are satisfied with the planned changes, apply the infrastructure modifications by running **terraform apply**. Terraform will prompt for confirmation before making any changes.

**Review and Validate the Infrastructure:** Once the Terraform apply command completes, review the created infrastructure to ensure it matches your expectations. Verify that the resources have been provisioned correctly.

**Cleanup and Destroy the Infrastructure (Optional):** If you want to clean up the resources created by Terraform, run **terraform destroy**. This command will prompt for confirmation before destroying the resources.

**How to test the API:**
Open AWS Console and select EC2. In EC2, select Loadbalancer. The Load Balancer will have 4 listener rules:

![image](https://github.com/paulkannan/serverless-solution-enable-fixed-response-loadbalancer/assets/46925641/f21729bb-bf2e-4afb-b977-1a984db10a68)

Open AWS Console and choose API Gateway. The API Gateway has 2 methods /maint and /original. Select PUT under /maint and Click on Test

![image](https://github.com/paulkannan/serverless-solution-enable-fixed-response-loadbalancer/assets/46925641/b57687b1-7220-43b5-833d-d47db84fd8b2)

It will trigger apply503 Lambda function and the user can validate the change of rules priority of fixed response code to 1 in listener rule:

![image](https://github.com/paulkannan/serverless-solution-enable-fixed-response-loadbalancer/assets/46925641/e50009d3-6c0d-4f14-ae51-bf6ff48eea36)

If /original PUT is triggered it will trigger revert503 Lambda Function and the fixed response will revert back to Priority 3.


