#!/bin/bash

#change rule priority 1 to 4 and 3 to 1
aws elbv2 set-rule-priorities \
  --cli-input-json '{    
    "RulePriorities": [
      {
        "RuleArn": "arn:aws:elasticloadbalancing:us-east-1:143173744693:listener-rule/app/cldfm-LoadB-KWZLIXM2JGIE/5dbdf0d50adad43f/dfa2480f2846a52f/acb16a5a67c41044",
        "Priority": 3
      },
      {
        "RuleArn": "arn:aws:elasticloadbalancing:us-east-1:143173744693:listener-rule/app/cldfm-LoadB-KWZLIXM2JGIE/5dbdf0d50adad43f/dfa2480f2846a52f/399e2363f837e57e",
        "Priority": 1
      }
      ]
  }'

