import math
import random
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Lambda = 2.25
# mew = 8.98
# A = 55
# M = 1994
# Z0 = 10112166  #ZO initial value
# C = 9
# a = 1  #priority limit
# b = 3  #priority limit
Lambda = 0
mew = 0
A = 0
M = 0
Z0 = 0  # ZO initial value
C = 0
a = 1  # priority limit
b = 3  # priority limit


def CP(Lambda):
    array = []
    i = 1
    total = 0
    num_of_cust = 0
    while total != 1:
        total = 0
        for x in range(0, i):
            temp = ((Lambda**x) * (math.e**-Lambda)) / math.factorial(x)
            total += temp
        array.append(total)
        i += 1
        num_of_cust += 1
    return array, num_of_cust


def CPlookUp(Lambda, num_of_cust):
    array = []
    for i in range(0, num_of_cust):
        total = 0
        for x in range(0, i):
            temp = ((Lambda**x) * (math.e**-Lambda)) / math.factorial(x)
            total += temp
        array.append(total)
    return array


def InterArrival(CP, CPlo, num_of_cust):
    IA = []
    for j in range(1, num_of_cust):
        temp = random.random()
        for i in range(0, num_of_cust - 1):
            if temp < CP[i] and temp > CPlo[i]:
                IA.append(i)
    return IA


def Arrivals(arrivals, IA, num_of_cust):
    temp = 0
    for i in range(0, num_of_cust - 1):
        temp += IA[i]
        arrivals.append(temp)


def Service(num_of_cust):
    service = []
    for i in range(0, num_of_cust):
        temp = -mew * math.log(random.random())
        service.append(round(temp))
    return service


def generate_priority(A, M, Z0, C, a, b, num_of_cust):
    Z = [Z0]
    R = []
    RanNum = []
    GP = []
    print(A, M, Z0, C)
    for i in range(0, num_of_cust):
        temp = (A * (Z[i]) + C) % M
        Z.append(temp)
        R.append(Z[i + 1])
        RanNum.append(R[i] / M)
        priority = a + RanNum[i] * (b - a)
        GP.append(round(priority))
    Z.remove(Z[-1])
    return Z, R, RanNum, GP


def qeueing(A, M, Z0, C, a, b, num_of_cust, arrivals, service):
    Z, R, RanNum, GP = generate_priority(A, M, Z0, C, a, b, num_of_cust)
    arrived = []
    labels = []
    for i in range(len(arrivals)):
        arrived.append(
            {
                "name": f"Process {i + 1}",
                "arrival_time": arrivals[i],
                "service_time": service[i],
                "priority": GP[i],
            }
        )
        labels.append(f"Name {i+1}")

    starts = []
    width = []
    #   table = PrettyTable([
    #     "Name", "Arrival Time", "Service Time", "Priority", "Service Start Time",
    #     "Service End Time", "Turnaround Time", "Wait Time", "Response Time"
    #         ])
    time = 0
    n = len(arrived)
    executed = 0
    current = 0
    waiting_queue = []
    executed_processes = set()
    remaining_times = {
        p["name"]: [p["service_time"], p["priority"], None, 0] for p in arrived
    }
    total_service_time = 0
    total_busy_time = 0
    gantt = [{"endTime": arrived[0]["arrival_time"], "name": "start", "priority": 0}]

    while executed < n:
        for p in arrived:
            if p["arrival_time"] == time and p["name"] not in executed_processes:
                waiting_queue.append(p)

                if (not current) or (
                    waiting_queue
                    and remaining_times[p["name"]][1]
                    < remaining_times[current["name"]][1]
                ):
                    if current:
                        print(current)
                        print(
                            "\n"
                            f"Leaving {current['name']} and Switching to process {p['name']} due to priority."
                            "\n"
                        )
                        gantt.append(
                            {
                                "endTime": time,
                                "name": current["name"],
                                "priority": current["priority"],
                            }
                        )
                    current = p

        if not current and waiting_queue:
            current = min(waiting_queue, key=lambda x: remaining_times[x["name"]][1])

        if not current and not waiting_queue:
            gantt.append({"endTime": time, "name": "Server Idle", "priority": 0})
            print("\n" f"Time {time}: Server is idle." "\n")

        if current:
            print(f"Time {time}: Executing {current['name']}")

            if remaining_times[current["name"]][2] == None:
                remaining_times[current["name"]][2] = time  # Service start time
            remaining_times[current["name"]][0] -= 1
            total_service_time += 1
            total_busy_time += 1
            if remaining_times[current["name"]][0] <= 0:
                print(current)
                gantt.append(
                    {
                        "endTime": time,
                        "name": current["name"],
                        "priority": current["priority"],
                    }
                )
                executed_processes.add(current["name"])
                remaining_times[current["name"]][3] = time + 1  # Service end time
                waiting_queue = [
                    p for p in waiting_queue if p["name"] != current["name"]
                ]

                turnaround_time = (
                    remaining_times[current["name"]][3] - current["arrival_time"]
                )

                wait_time = max(turnaround_time - current["service_time"], 0)

                response_time = (
                    remaining_times[current["name"]][2] - current["arrival_time"]
                )

                # table.add_row(
                #     [
                #         current["name"],
                #         current["arrival_time"],
                #         current["service_time"],
                #         current["priority"],
                #         remaining_times[current["name"]][
                #             2
                #         ],  # table index 4 and 5 have start and end time respectively
                #         remaining_times[current["name"]][3],
                #         turnaround_time,
                #         wait_time,
                #         response_time,
                #     ]
                # )
                width.append(
                    remaining_times[current["name"]][3]
                    - remaining_times[current["name"]][2]
                )
                starts.append(remaining_times[current["name"]][2])
                current = None
                executed += 1

        time += 1
    server_utilization_rate = total_busy_time / time

    #   print(table)
    #   plt.barh(range(len(labels)), width, left=starts, tick_label=labels)
    #   plt.show()
    # print("\n")
    # print(f"\nTotal Service Time: {total_service_time}")

    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0

    for p in arrived:
        if p["name"] in executed_processes:
            turnaround_time = remaining_times[p["name"]][3] - p["arrival_time"]
            wait_time = max(turnaround_time - p["service_time"], 0)
            response_time = remaining_times[p["name"]][2] - p["arrival_time"]

            total_waiting_time += wait_time
            total_turnaround_time += turnaround_time
            total_response_time += response_time

    # Calculate averages
    average_waiting_time = total_waiting_time / n
    average_turnaround_time = total_turnaround_time / n
    average_response_time = total_response_time / n

    # Print the results
    for item in gantt:
        print(item)

    print("\n")
    print(f"Average Waiting Time: {average_waiting_time:.2f}")
    print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
    print(f"Average Response Time: {average_response_time:.2f}")
    print(f"\nServer Utilization Rate: {server_utilization_rate * 100:.2f} %")
    return gantt


@app.route("/post_data", methods=["POST"])
def post_data():
    # Get the JSON data from the request
    data = request.get_json()

    # Process the data (you can do whatever you want with it)
    result = {"message": "Data received successfully", "data": data}

    # Return a JSON response
    return jsonify(result)


@app.route("/getGanttData")
def main():
    Lambda = float(request.args.get("lamb"))
    mew = float(request.args.get("mew"))
    A = int(request.args.get("A"))
    M = int(request.args.get("M"))
    Z0 = int(request.args.get("Z0"))
    C = int(request.args.get("C"))
    arr1, num_of_cust = CP(Lambda)
    arr2 = CPlookUp(Lambda, num_of_cust)
    IA = InterArrival(arr1, arr2, num_of_cust)
    arrivals = [0]
    Arrivals(arrivals, IA, num_of_cust)
    IA.insert(0, 0)
    service = Service(num_of_cust)
    gantt = qeueing(A, M, Z0, C, a, b, num_of_cust, arrivals, service)
    return gantt


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()  # This contains the form data
    # Process the data as needed
    Lambda = data["Lambda"]
    mew = data["mew"]
    A = data["A"]
    M = data["M"]
    Z0 = data["Zo"]  # ZO initial value
    C = data["C"]
    print(f"Received data: {data}")
    return f"Received data: {data}"


if __name__ == "__main__":
    # main()
    app.run(debug=True)
