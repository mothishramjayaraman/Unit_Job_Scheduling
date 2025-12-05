
from datetime import datetime, timedelta
from typing import Optional





# US6: Unit Idle-Time Optimization (Optimization)
def us6_optimize_idle_time(self, idle_unit):
    if idle_unit.status != "Idle": return None
    for q_name in ["Analysis", "Standard"]:
        if self.queues[q_name]:
            job_to_pull = self.queues[q_name].pop(0)
            job_to_pull.status = "Running"
            idle_unit.status = "Busy"
            print(f"--> [US6] Unit {idle_unit.id} was idle, pulled Job {job_to_pull.id} from {q_name}.")
            return job_to_pull
    return None


# US1: Unit Load Forecasting (Proactive Planning)
def us1_predict_load(self, unit):
    loads = unit.historical_loads
    if len(loads) < 2: return loads[-1]
    avg_increase = (loads[-1] - loads[0]) / len(loads)
    predicted_load = loads[-1] + avg_increase
    return round(predicted_load, 2)