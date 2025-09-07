const priority_cells = document.querySelectorAll(".priority");

priority_cells.forEach(cell => {
    if (cell.innerText.trim() === "1") {
        cell.innerText = "Urgent";
    } else if (cell.innerText.trim() === "2") {
        cell.innerText = "High";
    } else if (cell.innerText.trim() === "3") {
        cell.innerText = "Medium";
    } else if (cell.innerText.trim() === "4") {
        cell.innerText = "Low";
    }
});
