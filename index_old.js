var state;
const mM2 = () => {
    console.log("mm2")
    document.getElementById("lambda-mu-container").hidden = true
    document.getElementById("service-time-container").hidden = true
    document.getElementById("variance-of-arrival").hidden = true
    document.getElementById("mean-service-time").hidden = true
    document.getElementById("variance-of-service").hidden = true
    document.getElementById("variance-container").hidden = true
    document.getElementById("alpha-container").hidden = true

    document.getElementById("lambda-mu-container").hidden = false
    document.getElementById("service-time-container").hidden = false

    state = "mm2"
}

const mG2 = () => {
    console.log("mg2")
    document.getElementById("lambda-mu-container").hidden = true
    document.getElementById("service-time-container").hidden = true
    document.getElementById("variance-of-arrival").hidden = true
    document.getElementById("mean-service-time").hidden = true
    document.getElementById("variance-of-service").hidden = true
    document.getElementById("variance-container").hidden = true
    document.getElementById("alpha-container").hidden = true

    document.getElementById("lambda-mu-container").hidden = false
    document.getElementById("mean-service-time").hidden = false
    document.getElementById("variance-of-arrival").hidden = false
    state = "mg2"
}

const gG2 = () => {
    console.log("gg2")
    document.getElementById("lambda-mu-container").hidden = true
    document.getElementById("service-time-container").hidden = true
    document.getElementById("variance-of-arrival").hidden = true
    document.getElementById("mean-service-time").hidden = true
    document.getElementById("variance-of-service").hidden = true
    document.getElementById("variance-container").hidden = true
    document.getElementById("alpha-container").hidden = true

    document.getElementById("lambda-mu-container").hidden = false
    document.getElementById("mean-service-time").hidden = false
    document.getElementById("variance-of-arrival").hidden = false
    document.getElementById("variance-of-service").hidden = false
    state = "gg2"

}

const calculate_p0 = (rho) => {
    let summation = 0;
    for (let m = 0; m <= 2; m++) {
        summation += Math.pow(2 * rho, m) / factorial(m);
    }
    let p0 = 1 / (summation + (Math.pow(2 * rho, 2) / factorial(2)) * (1 - rho));
    return p0;
};

// Helper function to calculate factorial
function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    }
    return n * factorial(n - 1);
}




const calcmm2 = () => {
    arrival_rate = document.getElementById("lambda").value
    console.log(arrival_rate)

    service_rate = document.getElementById("stc").value

    utilization = arrival_rate / service_rate
    p0 = 1 / (1 + utilization)
    lq = utilization ** 2 / (1 - utilization)
    wq = lq / arrival_rate
    w = wq + (1 / service_rate)
    l = arrival_rate * w

    results = {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
    }

    var count = 1

    for (var key in results) {
        if (results.hasOwnProperty(key)) {
            var div = document.getElementById(`${count.toString()}`)
            var stringg = key + ": " + results[key].toString()
            div.textContent = stringg;
            count += 1
        }
    }
}

const calcmg2 = () => {
    arrival_rate = document.getElementById("lambda").value
    mean_service_time = document.getElementById("mst").value
    variance_service_time = document.getElementById("vof").value

    utilization = arrival_rate / (2 * mean_service_time)
    p0 = calculate_p0(utilization)
    lq = (p0 * utilization * (arrival_rate / mean_service_time) ** 2) / (2 * (1 - utilization) ** 2)
    wq = lq / arrival_rate
    w = wq + (1 / mean_service_time)
    l = arrival_rate * w

    results = {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
    }

    var count = 1

    for (var key in results) {
        if (results.hasOwnProperty(key)) {
            var div = document.getElementById(`${count.toString()}`)
            var stringg = key + ": " + results[key].toString()
            div.textContent = stringg;
            count += 1
        }
    }
}

const calcgg2 = () => {
    arrival_rate = document.getElementById("lambda").value
    service_rate = document.getElementById("stc").value
    var_arrival_time = document.getElementById("voa").value
    var_service_time = document.getElementById("vof").value

    utilization = arrival_rate / service_rate
    p0 = calculate_p0(utilization)
    lq = utilization ** 2 * (var_arrival_time + var_service_time) / (2 * service_rate ** 2 * (1 - utilization) ** 2)
    wq = lq / arrival_rate
    w = wq + (1 / service_rate)
    l = arrival_rate * w

    results = {
        'Utilization': utilization,
        'Probability of zero customers': p0,
        'Average number of customers in the system': l,
        'Average number of customers in the queue': lq,
        'Average waiting time in the system': w,
        'Average waiting time in the queue': wq
    }


    var count = 1

    // Loop through the object


    for (var key in results) {
        if (results.hasOwnProperty(key)) {
            var div = document.getElementById(`${count.toString()}`)
            var stringg = key + ": " + results[key].toString()
            div.textContent = stringg;
            count += 1
        }
    }
}

const calculate = () => {
    console.log("arrival_rate")
    if (state == "mm2") {
        calcmm2()
    }
    else if (state == "mg2") {
        calcmg2()
    }
    else if (state == "gg2") {
        calcgg2()
    }

}

function submitForm() {
    // ... your processing logic ...
    console.log("entered")
    const data = {
        Lambda: document.getElementById('lambda').value,
        mew: document.getElementById('mew').value,
        A: document.getElementById('A').value,
        M: document.getElementById('M').value,
        C: document.getElementById('C').value,
        a: document.getElementById('a').value,
        b: document.getElementById('b').value,
        Zo: document.getElementById('Zo').value
    }
    // fetch("http://127.0.0.1:5000/calculate", {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         // Add any other headers if needed
    //     },
    //     body: JSON.stringify(data) // Convert your data to JSON format
    // })
    //     .then((data) => {

    //     })
    //     .catch(error => console.error('Error:', error));
    fetch(`http://127.0.0.1:5000/getGanttData?lamb=${data.Lambda}&mew=${data.mew}&A=${data.A}&M=${data.M}&Z0=${data.Zo}&C=${data.C}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let container = document.getElementById("container")
            data.forEach((item, index) => {
                if (item.name == "start") {
                    container.innerHTML += `<div class="elementsTime">${item.endTime}</div>
                    `;
                }
                if (item.name == "Server Idle" && data[index + 1].name != "Server Idle") {
                    container.innerHTML += `
                <div class="element ${item.priority == 1 ? `reditem` : item.priority == 2 ? `yellowitem` : item.priority == 0 ? `grayitem` : `greenitem`}">${item.name}</div>
                <div class="elementsTime">${item.endTime}</div>
            `;
                }
                else if (item.name == "Server Idle" && data[index + 1].name == "Server Idle") {
                }

                else {

                    container.innerHTML += `
                    <div class="element ${item.priority == 1 ? `reditem` : item.priority == 2 ? `yellowitem` : item.priority == 0 ? `grayitem` : `greenitem`}">${item.name}</div>
                    <div class="elementsTime">${item.endTime}</div>
                `;
                }
            })
        })
        .catch(error => {
            console.error('Error:', error)
        });

}
