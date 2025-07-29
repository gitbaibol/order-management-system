// Function to initialize form event handlers
function initializeOrderForm() {
    const orderForm = document.getElementById('orderForm');
    const addOrderBtn = document.getElementById('addOrderBtn');
    const orderFormsContainer = document.getElementById('orderFormsContainer');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');

    if (addOrderBtn) {
        addOrderBtn.addEventListener('click', function() {
            const forms = orderFormsContainer.getElementsByClassName('order-form');
            const formCount = forms.length;
            const template = forms[0].cloneNode(true);
            
            // Update form index
            template.innerHTML = template.innerHTML.replaceAll(
                /form-(\d+)/g,
                `form-${formCount}`
            );

            // Update order number display
            const orderNumber = template.querySelector('.order-number');
            if (orderNumber) {
                orderNumber.textContent = formCount + 1;
            }

            // Clear form values
            template.querySelectorAll('input:not([type="hidden"]), select, textarea').forEach(input => {
                if (input.type === 'checkbox') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });

            // Show remove button for new form
            const removeBtn = template.querySelector('.remove-order');
            if (!removeBtn) {
                const orderHeader = template.querySelector('.d-flex');
                if (orderHeader) {
                    const newRemoveBtn = document.createElement('button');
                    newRemoveBtn.type = 'button';
                    newRemoveBtn.className = 'btn btn-danger btn-sm remove-order';
                    newRemoveBtn.innerHTML = '<i class="fas fa-times"></i> Удалить';
                    orderHeader.appendChild(newRemoveBtn);
                }
            }

            // Add the new form
            orderFormsContainer.appendChild(template);
            
            // Update total forms count
            totalForms.value = formCount + 1;
        });
    }

    // Handle remove buttons using event delegation
    if (orderFormsContainer) {
        orderFormsContainer.addEventListener('click', function(e) {
            if (e.target.closest('.remove-order')) {
                const formDiv = e.target.closest('.order-form');
                if (formDiv) {
                    // If this form has a delete checkbox (for existing orders), mark it as deleted
                    const deleteCheckbox = formDiv.querySelector('.delete-field');
                    if (deleteCheckbox) {
                        deleteCheckbox.checked = true;
                        formDiv.style.display = 'none';
                    } else {
                        // For new forms, just remove the div
                        formDiv.remove();
                        const forms = orderFormsContainer.getElementsByClassName('order-form');
                        // Update total forms count
                        totalForms.value = forms.length;
                        // Update order numbers
                        Array.from(forms).forEach((form, index) => {
                            const orderNumber = form.querySelector('.order-number');
                            if (orderNumber) {
                                orderNumber.textContent = index + 1;
                            }
                        });
                    }
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeOrderForm);
