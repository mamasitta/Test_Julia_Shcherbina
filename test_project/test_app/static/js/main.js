
function PutData (e) {
    e.preventDefault();
    var butNum = document.getElementById('buttonAddColumn').value
    var name_id = parseInt(butNum, 10);

    var name = document.getElementById("name").value;
    var type = document.getElementById("type").value;
    if (type === "Integer") {
        var newCellRangeFrom = document.createElement("td")
        var tBoxRangeFrom = document.createElement("input")
        tBoxRangeFrom.setAttribute('type', 'number');
        tBoxRangeFrom.setAttribute("name", "range_from"+name_id);
        tBoxRangeFrom.setAttribute('class', "item");
        newCellRangeFrom.appendChild(tBoxRangeFrom)
        var newCellRangeTill = document.createElement("td")
        var tBoxRangeTill = document.createElement('input')
        tBoxRangeTill.setAttribute('type', 'number');
        tBoxRangeTill.setAttribute("name", "range_till"+name_id);
        tBoxRangeTill.setAttribute('class', "item");
        newCellRangeTill.appendChild(tBoxRangeTill)
    }
    else{
        var newCellRangeFrom = document.createElement('td')
        newCellRangeFrom.setAttribute("style", "empty-cells: show;");
        newCellRangeFrom.innerHTML = "&nbsp"
        var newCellRangeTill = document.createElement('td')
        newCellRangeTill.setAttribute("style", "empty-cells: show;");
        newCellRangeTill.innerHTML  = "&nbsp"

    }
    var order = document.getElementById('order').value;
    var newRow = document.createElement("tr");
    newRow.setAttribute("id", name_id)

    var newCellOrder = document.createElement("td");
    var tBoxOrder = document.createElement('input');
    tBoxOrder.setAttribute('type', 'number');
    tBoxOrder.setAttribute('value', order);
    tBoxOrder.setAttribute("name", "order"+name_id);
    tBoxOrder.setAttribute('class', "item");
    newCellOrder.appendChild(tBoxOrder)
    console.log(newCellOrder)

    var newCellName = document.createElement("td");
    var tBoxName = document.createElement('input');
    tBoxName.setAttribute('type', 'text');
    tBoxName.setAttribute('value', name);
    tBoxName.setAttribute('name', 'name'+name_id);
    tBoxName.setAttribute('class', 'item');
    newCellName.appendChild(tBoxName);

    var newCellType = document.createElement("td");
    var tBoxType = document.createElement("input");
    tBoxType.setAttribute('type', 'text');
    tBoxType.setAttribute('value', type);
    tBoxType.setAttribute('name', 'type'+name_id);
    tBoxType.setAttribute('class', 'item');
    newCellType.appendChild(tBoxType)

    var newDelete = document.createElement('td')
    var boxDelete = document.createElement("a")
    var boxDelete1 = document.createElement('h5')
    boxDelete1.setAttribute("class", 'delete')
    boxDelete1.setAttribute("value", name_id)
    boxDelete1.setAttribute("id", name_id)
    boxDelete1.setAttribute("onclick", "DeleteColumn(this);")
    boxDelete1.innerHTML = "Delete"
    boxDelete.appendChild(boxDelete1)
    newDelete.appendChild(boxDelete)
    console.log(newDelete)

    newRow.append(newCellName, newCellType, newCellRangeFrom, newCellRangeTill, newCellOrder, newDelete);
    document.getElementById("rows").appendChild(newRow);
    document.getElementById("name").value = '';
    document.getElementById("order").value = '';
    name_id = name_id + 1
    document.getElementById('buttonAddColumn').value = name_id
    document.getElementById('add_number').value = name_id

    console.log(document.getElementById('add_number'))
}
function DeleteColumn(btn) {
    var row = btn.parentNode.parentNode;
    row.parentNode.remove(row);

}
