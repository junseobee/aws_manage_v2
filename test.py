from aws_connection import  account_service




def get_cw_metrics(account):
    metrics = ["CPUUtilization", "StatusCheckFailed", "disk_used_percent", 
                "LogicalDisk % Free Space", "mem_used_percent", "Memory Available MBytes"]
    cw_metrics = []
    object = account_service(account_name=account, service_name="cloudwatch")
    

    # List metrics (replace the filters with your own criteria)
    response = object.service.list_metrics(
        # Namespace='AWS/EC2',  # Replace with your desired namespace
        # MetricName='CPUUtilization',  # Replace with your desired metric name
        Dimensions=[{'Name': 'InstanceId', 'Value': 'i-098a2df8b3268406d'}]  # Replace with your desired dimensions
    )


    # Print the list of metrics
    for metric in response['Metrics']:
        if metric["MetricName"] in metrics:
            if metric["MetricName"] == "disk_used_percent":
                if "tmpfs" not in metric["Dimensions"][-1]["Value"]:
                    cw_metrics.append(metric)
            else:
                cw_metrics.append(metric)
            
    
    return cw_metrics



cw_metrics = get_cw_metrics("avon_qde")
for metric in cw_metrics:
    # metric["alarm_name"] = f"CRITICAL-{instance_name}-CPU-{instance_id}"
    # metric["alarm_description"] = f"Critical CPU Alarm Setting for {instance_name}"
    metric["comparison_operator"] = 1
    metric["evaluation_periods"] = 2
    metric["threshold"] = 3
    metric["period"] = 4
    metric["action"] = 5
    print(metric)
    device = [item["Value"] for item in metric["Dimensions"] if item["Name"] == "instance"]
    if len(device) == 1:
        print(device[0])




''''
cpu
        AlarmName = alarm["alarm_name"],
        AlarmDescription = alarm["alarm_description"],
        ComparisonOperator = alarm["comparison_operator"],
        EvaluationPeriods = alarm["evaluation_periods"],
        Threshold = alarm["threshold"],
        Namespace = "AWS/EC2",
        MetricName = "CPUUtilization",
        Period = alarm["period"],
        Statistic = "Average",
        ActionsEnabled = True,
        AlarmActions = [alarm["action"]],
        OKActions = [alarm["action"]],
        Dimensions = [
status
        AlarmName = alarm["alarm_name"],
        AlarmDescription = alarm["alarm_description"],
        ComparisonOperator = alarm["comparison_operator"],
        EvaluationPeriods = alarm["evaluation_periods"],
        Threshold = alarm["threshold"],
        Namespace = "AWS/EC2",
        MetricName = "StatusCheckFailed",
        Period = alarm["period"],
        Statistic = "Average",
        ActionsEnabled = True,
        AlarmActions = [alarm["action"]],
        OKActions = [alarm["action"]],
        Dimensions = [

disk linux
        AlarmName = f'{alarm["alarm_name"]}-{params["device"]}',
        AlarmDescription = alarm["alarm_description"],
        MetricName = "disk_used_percent",
        Namespace = "CWAgent",
        Statistic="Average",
        Period=alarm["period"],
        ActionsEnabled=True,
        AlarmActions=[alarm["action"]],
        OKActions=[alarm["action"]],
        Threshold=alarm["threshold"],
        ComparisonOperator = alarm["comparison_operator"],
        EvaluationPeriods = alarm["evaluation_periods"],
        Dimensions=dimensions,
disk windows
        AlarmName= f'{alarm["alarm_name"]}-{device.replace(":", "")}',
        AlarmDescription=alarm["alarm_description"],
        MetricName="LogicalDisk % Free Space",
        Namespace="CWAgent",
        Statistic="Average",
        Period=alarm["period"],
        ActionsEnabled=True,
        AlarmActions=[alarm["action"]],
        OKActions=[alarm["action"]],
        Threshold=alarm["threshold"],
        ComparisonOperator = alarm["comparison_operator"],
        EvaluationPeriods = alarm["evaluation_periods"],
        Dimensions=dimensions,

memory linux
        AlarmName=alarm["alarm_name"],
        AlarmDescription=alarm["alarm_description"],
        ComparisonOperator=alarm["comparison_operator"],
        EvaluationPeriods=alarm["evaluation_periods"],
        Threshold=alarm["threshold"],
        Namespace='CWAgent',
        MetricName='mem_used_percent',
        Period=alarm["period"],
        Statistic="Average",
        ActionsEnabled=True,
        AlarmActions=[alarm["action"]],
        OKActions=[alarm["action"]],
        Dimensions=dimensions

memory windows
        AlarmName=alarm["alarm_name"],
        AlarmDescription=alarm["alarm_description"],
        ComparisonOperator=alarm["comparison_operator"],
        EvaluationPeriods=alarm["evaluation_periods"],
        Threshold=alarm["threshold"],
        Namespace='CWAgent',
        MetricName='Memory Available MBytes',
        Period=alarm["period"],
        Statistic='Average',
        ActionsEnabled=True,
        AlarmActions=[alarm["action"]],
        OKActions=[alarm["action"]],
        Dimensions=dimensions

                
'''