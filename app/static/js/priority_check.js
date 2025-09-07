const priority_cells = document.querySelectorAll(".badge");
const status_cells = document.querySelectorAll(".status")

priority_cells.forEach(cell => {
    const text = cell.innerText.trim();

     if (text.includes("1")) {
        cell.innerText = text.replace("1", "Urgent");
    } else if (text.includes("2")) {
        cell.innerText = text.replace("2", "High");
    } else if (text.includes("3")) {
        cell.innerText = text.replace("3", "Medium");
    } else if (text.includes("4")) {
        cell.innerText = text.replace("4", "Low");
    }
});

status_cells.forEach(cell => {
    const text = cell.innerHTML.trim()
    if (text.includes("completed")){
        cell.style.backgroundColor = "#28a745"
    } else if (text.includes("in_progress")) {
        cell.style.backgroundColor = "#17a2b8"
    } else {
        cell.style.backgroundColor = "#ffc107"
    }
})