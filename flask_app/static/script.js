document.addEventListener("DOMContentLoaded", function () {
    const deleteForms = document.querySelectorAll("form.delete-form");
    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault(); // ป้องกันการส่งฟอร์มทันที

            const confirmed = confirm("Are you sure you want to delete this comment?");
            if (confirmed) {
                form.submit(); // ถ้ายืนยัน ก็จะส่งฟอร์มลบจริง
            }
        });
    });
});
