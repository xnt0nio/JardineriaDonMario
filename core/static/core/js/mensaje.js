function mensaje() {
    alert('Bienvenido a la pagina');
}

function deleteProducto(id) {
    //alert(id);
    //console.log("ID: "+id);
    Swal.fire({
        title: 'Eliminar',
        text: '¿Desea eliminar producto?',
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Eliminar'
      }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire('Eliminado!','Producto Eliminado Correctamente','success').then(function() {
                window.location.href = "/delete/"+id+"/";
            })
        }
      })
}

function eliminar_producto(id) {
    //alert(id);
    //console.log("ID: "+id);
    Swal.fire({
        title: 'Eliminar',
        text: '¿Desea eliminar producto del carrito?',
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Eliminar'
      }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire('Eliminado!','Producto Eliminado Correctamente','success').then(function() {
                window.location.href = "/eliminar_producto/"+id+"/";
            })
        }
      })
}






  
  
  
  
