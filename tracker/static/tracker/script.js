document.addEventListener('DOMContentLoaded', () => {
    // Update and Delete Income Buttons
    const editIncomeButtons = document.querySelectorAll('.edit-income-btn');
    const deleteIncomeButtons = document.querySelectorAll('.delete-income-btn');

    editIncomeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const incomeId = button.getAttribute('data-id');
            window.location.href = `/edit_income/${incomeId}/`;
        });
    });

    deleteIncomeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const incomeId = button.getAttribute('data-id');
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(`/delete_income/${incomeId}/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken },
            })
            .then(response => {
                if (response.ok) {
                    // button.parentNode.remove();
                    const incomeEntry = button.closest('li');
                    incomeEntry.remove();
                } else {
                    console.error('Error deleting income');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Update and Delete Expense Buttons
    const editExpenseButtons = document.querySelectorAll('.edit-expense-btn');
    const deleteExpenseButtons = document.querySelectorAll('.delete-expense-btn');

    editExpenseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const expenseId = button.getAttribute('data-id');
            window.location.href = `/edit_expense/${expenseId}/`;
        });
    });

    deleteExpenseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const expenseId = button.getAttribute('data-id');
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(`/delete_expense/${expenseId}/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken },
            })
            .then(response => {
                if (response.ok) {
                    // button.parentNode.remove();
                    const expenseEntry = button.closest('li');
                    expenseEntry.remove();
                } else {
                    console.error('Error deleting expense');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
