/**
 * Recoge los comentarios del Arsenal de Corona de Hielo en esta hoja.
 *
 * CÓMO SE INSTALA
 *   1. Abre la hoja de cálculo donde quieres los comentarios.
 *   2. Extensiones → Apps Script. Borra lo que haya y pega este fichero entero.
 *   3. Guarda (💾) y ponle nombre al proyecto.
 *   4. Implementar → Nueva implementación → tipo «Aplicación web».
 *        Ejecutar como:   Yo
 *        Quién tiene acceso: Cualquier usuario
 *      Google pedirá autorización la primera vez; es normal, es tu propio
 *      script escribiendo en tu propia hoja.
 *   5. Copia la URL que termina en /exec y pásasela a quien monta el sitio.
 *
 * La hoja se prepara sola: si está vacía, la primera visita crea la fila de
 * cabeceras.
 */

// La hoja donde se escriben los comentarios, por su identificador: es el trozo
// largo de su URL, entre /d/ y /edit. Poniéndolo aquí da igual si el script se
// creó desde dentro de la hoja o suelto en script.google.com.
var HOJA = '1r9xoC12FC9of2p0aTcQOvuvdhb-f71PsEho_tiltoGI';

// Si pones aquí una palabra cualquiera, el sitio tendrá que enviarla también y
// los envíos que no la traigan se descartan. No es un secreto —viaja en la
// página— pero corta los robots que rastrean formularios sueltos.
var CLAVE = '';

var CABECERAS = ['Fecha', 'Clase', 'Especialización', 'Tema',
                 'Objeto o talento', 'Comentario', 'Nombre'];
var TOPE_COMENTARIO = 1200;


function doPost(e) {
  try {
    var p = (e && e.parameter) || {};

    if (CLAVE && p.clave !== CLAVE) {
      return respuesta('clave incorrecta');
    }
    var mensaje = (p.mensaje || '').toString().trim();
    if (!mensaje) {
      return respuesta('comentario vacío');
    }
    if (mensaje.length > TOPE_COMENTARIO) {
      mensaje = mensaje.slice(0, TOPE_COMENTARIO);
    }

    var hoja = SpreadsheetApp.openById(HOJA).getSheets()[0];
    if (hoja.getLastRow() === 0) {
      hoja.appendRow(CABECERAS);
      hoja.getRange(1, 1, 1, CABECERAS.length).setFontWeight('bold');
      hoja.setFrozenRows(1);
    }
    hoja.appendRow([
      new Date(),
      (p.clase || '').toString(),
      (p.espec || '').toString(),
      (p.tema || '').toString(),
      (p.cual || '').toString(),
      mensaje,
      (p.firma || '').toString().slice(0, 40)
    ]);
    return respuesta('ok');
  } catch (err) {
    return respuesta('error: ' + err);
  }
}


// Abrir la URL en el navegador sirve para comprobar que está viva.
function doGet() {
  return respuesta('El recogedor de comentarios está funcionando.');
}


function respuesta(texto) {
  return ContentService.createTextOutput(texto)
    .setMimeType(ContentService.MimeType.TEXT);
}
