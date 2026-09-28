       // --- VERIFICACIÓN DE SEGURIDAD (GUARDIA) ---
if (localStorage.getItem('sesionActiva') !== 'true') {
    // Si el usuario no tiene una sesión válida, lo rebotamos al login
    window.location.href = 'login.html';
}

// Función global para destruir la sesión
window.cerrarSesion = function() {
    localStorage.clear(); // Borra las credenciales del navegador
    window.location.href = 'login.html';
};
       // Función asíncrona para solicitar los datos al backend
        async function cargarMaterias() {
            try {
                // Hacemos la petición GET a la ruta que configuraste previamente
                const respuesta = await fetch('http://127.0.0.1:8000/materias/?skip=0&limit=50');
                
                if (!respuesta.ok) {
                    throw new Error("Error en la respuesta del servidor");
                }

                // Convertimos la respuesta a un arreglo JSON
                const materias = await respuesta.json();
                
                // Seleccionamos el cuerpo de la tabla en el HTML
                const tbody = document.getElementById('tabla-materias');
                tbody.innerHTML = ''; // Limpiamos contenido previo
                
                // Iteramos sobre cada materia y creamos una fila
                materias.forEach(materia => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${materia.id}</td>
                        <td><strong>${materia.clave}</strong></td>
                        <td>${materia.nombre}</td>
                        <td>${materia.creditos}</td>
                    `;
                    tbody.appendChild(fila);
                });

            } catch (error) {
                console.error("Hubo un fallo al conectar con la API:", error);
            }
        }

        // Ejecutar la función en cuanto cargue la página
        cargarMaterias();
        // Capturar el evento de envío del formulario
        document.getElementById('form-materia').addEventListener('submit', async function(evento) {
            evento.preventDefault(); // Evita que la página web se recargue al dar clic

            // Extraer los valores que el usuario escribió
            const nuevaMateria = {
                clave: document.getElementById('clave').value,
                nombre: document.getElementById('nombre').value,
                creditos: parseInt(document.getElementById('creditos').value)
            };

            try {
                // Enviar el JSON al backend mediante POST
                const respuesta = await fetch('http://127.0.0.1:8000/materias/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(nuevaMateria)
                });

                if (respuesta.ok) {
                    // Limpiar las cajas de texto
                    document.getElementById('form-materia').reset();
                    // Volver a consultar la base de datos para refrescar la tabla al instante
                    cargarMaterias();
                } else {
                    alert("Error: Verifica que la clave no esté duplicada.");
                }
            } catch (error) {
                console.error("Fallo al enviar los datos:", error);
            }
        });
        // --- LÓGICA PARA ALUMNOS ---

        // Función para consultar la base de datos y pintar la tabla de alumnos
        async function cargarAlumnos() {
            try {
                // Ahora solo hacemos UNA petición, el backend ya trae el JOIN de la matrícula
                const respuesta = await fetch('http://127.0.0.1:8000/alumnos/?skip=0&limit=50', { cache: 'no-store' });
                const alumnos = await respuesta.json();
                
                const tbody = document.getElementById('tabla-alumnos');
                tbody.innerHTML = ''; 
                
                alumnos.forEach(alumno => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${alumno.id}</td>
                        <td><strong>${alumno.matricula}</strong></td> 
                        <td><strong>${alumno.nombre}</strong></td>
                        <td>${alumno.apellidos}</td>
                    `;
                    tbody.appendChild(fila);
                });
            } catch (error) {
                console.error("Error al cargar alumnos:", error);
            }
        }
        
        // Evento para guardar un nuevo alumno de forma automatizada (Un solo POST)
                document.getElementById('form-alumno').addEventListener('submit', async function(evento) {
                    evento.preventDefault();

                    const matricula = document.getElementById('matricula').value;
                    const password = document.getElementById('password').value;
                    const nombre = document.getElementById('nombre-alumno').value;
                    const apellidos = document.getElementById('apellidos-alumno').value;

                    try {
                        // Enviamos todo en un solo paquete al backend automatizado
                        const resAlumno = await fetch('http://127.0.0.1:8000/alumnos/', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ 
                                matricula: matricula, 
                                password: password, 
                                nombre: nombre, 
                                apellidos: apellidos 
                            })
                        });

                        if (resAlumno.ok) {
                            document.getElementById('form-alumno').reset(); // Limpiar cajas de texto
                            cargarAlumnos(); // Refrescar la tabla al instante
                        } else {
                            alert("Error: Es posible que la matrícula ya esté registrada.");
                        }

                    } catch (error) {
                        console.error("Fallo general al registrar al alumno:", error);
                    }
                });

        // Ejecutar al inicio
        cargarAlumnos();

        // --- LÓGICA PARA CALIFICACIONES ---

        // Función para consultar y pintar la tabla de calificaciones
        async function cargarCalificaciones() {
            try {
                const respuesta = await fetch('http://127.0.0.1:8000/calificaciones/?skip=0&limit=50');
                const calificaciones = await respuesta.json();
                
                const tbody = document.getElementById('tabla-calificaciones');
                tbody.innerHTML = ''; 
                
                calificaciones.forEach(calif => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${calif.id}</td>
                        <td>${calif.alumno_nombre}</td>
                        <td>${calif.materia_nombre}</td>
                        <td>${calif.ciclo}</td>
                        <td><strong>${calif.valor}</strong></td>
                    `;
                    tbody.appendChild(fila);
                });
            } catch (error) {
                console.error("Error al cargar calificaciones:", error);
            }
        }

        // Evento para guardar una nueva calificación
        document.getElementById('form-calificacion').addEventListener('submit', async function(evento) {
            evento.preventDefault();

            // Pydantic exige que los IDs sean enteros y la calificación un flotante (decimal)
            const nuevaCalificacion = {
                alumno_id: parseInt(document.getElementById('id-alumno').value),
                materia_id: parseInt(document.getElementById('id-materia').value),
                ciclo: document.getElementById('ciclo').value,
                valor: parseFloat(document.getElementById('valor').value)
            };

            try {
                const respuesta = await fetch('http://127.0.0.1:8000/calificaciones/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(nuevaCalificacion)
                });

                if (respuesta.ok) {
                    document.getElementById('form-calificacion').reset(); // Limpia las cajas
                    cargarCalificaciones(); // Refresca la tabla al instante
                } else {
                    alert("Error: Verifica que el ID del Alumno y el ID de la Materia realmente existan en las tablas de arriba.");
                }
            } catch (error) {
                console.error("Fallo al enviar los datos:", error);
            }
        });

        // Ejecutar al inicio
        cargarCalificaciones();