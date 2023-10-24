fetch('http://127.0.0.1:5000/getGanttData')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        let container = document.getElementById("container")
        data.forEach((item, index) => {
            if (item.name == "Server Idle" && data[index + 1].name != "Server Idle") {
                container.innerHTML += `
                <div class="element ${item.priority == 1 ? `reditem` : item.priority == 2 ? `yellowitem` : `greenitem`}">${item.name}</div>
                <div class="elementsTime">${item.endTime}</div>
            `;
            }
            else if (item.name == "Server Idle" && data[index + 1].name == "Server Idle") {
            }
            else {

                container.innerHTML += `
                    <div class="element ${item.priority == 1 ? `reditem` : item.priority == 2 ? `yellowitem` : `greenitem`}">${item.name}</div>
                    <div class="elementsTime">${item.endTime}</div>
                `;
            }
        })
    })
    .catch(error => console.error('Error:', error));