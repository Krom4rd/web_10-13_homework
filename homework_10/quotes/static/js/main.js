async function confirmDelete(id) {
    const result = await Swal.fire({
        title: 'Ви впевнені?',
        text: 'Цю дію не можна скасувати!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Так, видалити!',
        cancelButtonText: 'Скасувати'
    });

    if (result.isConfirmed) {
        const deleteUrl = `/delete/${id}`;
        window.location.href = deleteUrl;
    }
}