from aws_connection import account_service, topic_arns


METRICS = [
    "CPUUtilization", 
    "StatusCheckFailed", 
    "disk_used_percent", 
    "LogicalDisk % Free Space", 
    "mem_used_percent", 
    "Memory Available MBytes"   
]


def put_cw_alarm(cw_client, alarm):

    cloudwatch = cw_client
    print(alarm["alarm_name"])
        
    # Create alarm
    cloudwatch.put_metric_alarm(
        AlarmName=alarm["alarm_name"],
        AlarmDescription=alarm["alarm_description"],
        ComparisonOperator=alarm["comparison_operator"],
        EvaluationPeriods=alarm["evaluation_periods"],
        Threshold=alarm["threshold"],
        Namespace=alarm["Namespace"],
        MetricName=alarm["MetricName"],
        Period=alarm["period"],
        Statistic='Average',
        ActionsEnabled=True,
        AlarmActions=[alarm["action"]],
        OKActions=[alarm["action"]],
        Dimensions=alarm["Dimensions"]
    )


def get_cw_metrics(client, instance_id):
    cw_metrics = []

    response = client.list_metrics(
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}] 
    )

    for metric in response["Metrics"]:
        if metric["MetricName"] in METRICS:
            if metric["MetricName"] == "disk_used_percent":
                if metric["Dimensions"][-1]["Value"] in ("xfs", "ext4"):
                    cw_metrics.append(metric)
            else:
                cw_metrics.append(metric)
    
    return cw_metrics


def set_cloudwatch_alarm(objects):
    #Parameters for creating alarms
    evaluation_periods = 1
    gte_operator = "GreaterThanOrEqualToThreshold"
    lte_operator = "LessThanOrEqualToThreshold"
    cpu_threshold = 90
    cpu_period = 300 #second
    status_threshold = 0.99
    status_period = 60
    disk_linux_period = 300
    disk_linux_threshold = 90
    disk_win_period = 300
    disk_win_threshold = 10
    memory_linux_period = 300
    memory_linux_threshold = 90
    memory_win_period = 300
    memory_win_threshold = 500

    # Set Alarms for the targets
    for object in objects:
        action = topic_arns[object.account]

        print("=" * 120)
        print(f"Account name: {object.account}")
        
        for content in object.contents:
            instance_id = content["id"]
            instance_name = content["name"]

            client_object = account_service(account_name=object.account, service_name="cloudwatch")
            cw_client = client_object.service
            cw_metrics = get_cw_metrics(cw_client, instance_id) # get Namespace, MetricName, Dimensions

            for metric in cw_metrics:
                metric["action"] = action
                metric["evaluation_periods"] = evaluation_periods

                # It would be better to be concise, but the names are following the naming rule.
                if metric["MetricName"] == "CPUUtilization":
                    metric["alarm_name"] = f"CRITICAL-{instance_name}-CPU-{instance_id}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - High CPU Utilization {cpu_threshold}%"
                    metric["comparison_operator"] = gte_operator
                    metric["threshold"] = cpu_threshold
                    metric["period"] = cpu_period
                    put_cw_alarm(cw_client, metric)
                elif metric["MetricName"] == "StatusCheckFailed":
                    metric["alarm_name"] = f"CRITICAL-{instance_name}-STATUS-{instance_id}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - STATUS Alarm"
                    metric["comparison_operator"] = gte_operator
                    metric["threshold"] = status_threshold
                    metric["period"] = status_period
                    put_cw_alarm(cw_client, metric)
                elif metric["MetricName"] == "disk_used_percent":
                    # All alarm names should be differnt. 
                    # So, the name are put its device name at the end of the name 
                    # because a server would be able to have more than one disk.
                    device = [ item["Value"] for item in metric["Dimensions"] if item["Name"] == "device" ]
                    if len(device) == 1:
                        metric["alarm_name"] = f"CRITICAL-{instance_name}-DISK-{instance_id}-{device[0]}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - High Disk {device[0]} Usage {disk_linux_threshold}%"
                    metric["comparison_operator"] = gte_operator
                    metric["threshold"] = disk_linux_threshold
                    metric["period"] = disk_linux_period
                    put_cw_alarm(cw_client, metric)
                elif metric["MetricName"] == "LogicalDisk % Free Space":
                    device = [item["Value"] for item in metric["Dimensions"] if item["Name"] == "instance"]
                    if len(device) == 1:
                        drive = device[0].replace(":", "")
                        metric["alarm_name"] = f"CRITICAL-{instance_name}-DISK-{instance_id}-{drive}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - Low Disk {drive} Free space {disk_win_threshold}%"
                    metric["comparison_operator"] = lte_operator
                    metric["threshold"] = disk_win_threshold
                    metric["period"] = disk_win_period
                    put_cw_alarm(cw_client, metric)
                elif metric["MetricName"] == "mem_used_percent":
                    metric["alarm_name"] = f"CRITICAL-{instance_name}-MEMORY-{instance_id}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - High Memory Usage {memory_linux_threshold}%"
                    metric["comparison_operator"] = gte_operator
                    metric["threshold"] = memory_linux_threshold
                    metric["period"] = memory_linux_period
                    put_cw_alarm(cw_client, metric)
                elif metric["MetricName"] == "Memory Available MBytes":
                    metric["alarm_name"] = f"CRITICAL-{instance_name}-MEMORY-{instance_id}"
                    metric["alarm_description"] = f"{instance_name} - {instance_id} - High Memory Usage {memory_win_threshold}%"
                    metric["comparison_operator"] = lte_operator
                    metric["threshold"] = memory_win_threshold
                    metric["period"] = memory_win_period
                    put_cw_alarm(cw_client, metric)
