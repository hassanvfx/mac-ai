# Playbook reutilizable: libro, repositorio y publicación impresa

Este documento captura un método repetible para libros técnicos, creativos,
educativos o de no ficción que se acompañan de código, ejercicios, archivos o
fuentes verificables. El objetivo es mantener libro, sitio, repositorio y PDF
en sincronía durante toda la vida del proyecto.

## El modelo que funciona

No escribas una versión para el libro, otra para el sitio y otra para el
repositorio. Usa capítulos Markdown como la única prosa publicada:

```text
investigación + evidencia + ejercicios
                 ↓
       capítulos Markdown canónicos
          ↙              ↘
 sitio/curso navegable   manuscrito DOCX/PDF
          ↓              ↓
     laboratorios      impresión y prueba
```

- `research/` conserva fuentes, bibliografía y decisiones de evidencia.
- `book/chapters/` conserva el texto canónico.
- `experiments/` o `exercises/` contiene lo que el lector ejecuta, adapta o
  verifica.
- `benchmarks/` o `evidence/` registra método, versiones, resultados y límites.
- `site/` es navegación y presentación: no duplica los capítulos.
- `book/build/` contiene artefactos generados y no debe ser fuente editorial.

Para un proyecto no técnico, un “ejercicio” puede ser un archivo de fuentes,
una cronología, una actividad de lectura o una plantilla de trabajo. El
principio es el mismo: cada promesa importante debe tener evidencia accesible.

## El puente lector → repositorio

Todo capítulo práctico necesita una ficha con: URL del laboratorio, ruta del
material fuente, comando o actividad, resultado esperado, evidencia y siguiente
paso. Almacena esos campos en un manifiesto único y genera desde él las páginas
del sitio, los QR y el panel final del capítulo. Así no se rompe el puente cuando
cambia una URL, una ruta o un ejercicio.

Los QR deben apuntar a una URL estable del curso, no a un archivo efímero. La
página de destino enlaza a `main`, explica cómo clonar el repositorio y muestra
la actividad exacta. El QR es un atajo para pasar del papel al teléfono y de
ahí a la computadora; siempre acompáñalo con una URL escrita legible.

## Pipeline de publicación determinista

Construye el libro siempre en este orden:

1. Validar capítulos, referencias, enlaces y manifiesto de laboratorios.
2. Generar DOCX desde Markdown canónico y una plantilla de impresión versionada.
3. Aplicar estilos de libro: márgenes, tipografía, párrafos, código, figuras y
   aperturas de capítulo.
4. Renderizar el interior y derivar el TOC de esa paginación real.
5. Añadir folios solo donde deben aparecer.
6. Construir el PDF maestro, preflight y revisión visual.
7. Guardar hashes, versiones, número de páginas y resultados en un manifiesto.

El TOC nunca se mantiene manualmente. Debe venir del mismo artefacto que se
empaqueta: una figura o un salto de página puede alterar todos los números.

Una secuencia de front matter robusta, cuando la cubierta exterior se prepara
por separado, es:

```text
portada visual interior → copyright/ISBN → dedicatoria → TOC → contenido
```

El ISBN se muestra como texto en copyright cuando aplica. El código de barras
pertenece a la cubierta exterior y a la zona segura de la plantilla final de la
imprenta, no al interior.

## Lecciones críticas de Lulu y la impresión bajo demanda

- **Fuentes:** que el PDF se vea bien no demuestra que sea imprimible. Audita
  cada fuente usada y exige *Embedded* o *Embedded Subset*. Evita recursos
  Base-14 accidentales, incluso si los agrega una librería y parecen invisibles.
- **Imágenes:** mide píxeles efectivos al tamaño de colocación. Una página 6×9
  a 300 ppi requiere 1800×2700 px. Un upscale conserva composición, pero no
  crea detalle; necesita prueba física antes de declararse definitivo.
- **Transparencia:** detecta máscaras alfa, `/SMask`, estados alfa y grupos de
  transparencia. Rasteriza únicamente las páginas afectadas a 300 ppi RGB para
  no degradar el libro entero.
- **Tinta:** fondos muy oscuros pueden generar advertencias en Color Standard.
  Distingue bloqueos técnicos de advertencias a juzgar en prueba física; no
  sustituyas una pieza visual aprobada por una versión peor solo para eliminar
  un aviso.
- **Bleed:** un interior sin sangrado debe tener exactamente el tamaño de corte.
  Si algo llega al borde, usa el tamaño con bleed definido por la imprenta. La
  cubierta final se construye solo después de congelar el número de páginas y
  recibir la plantilla exacta.
- **Render visual:** el preflight no detecta mala jerarquía tipográfica,
  diagramas ilegibles, viudas, huérfanas o códigos demasiado pequeños. Renderiza
  y revisa todas las páginas críticas, después ordena una prueba física.

## Qué automatizar y qué mantener humano

Automatiza los hechos objetivos: enlaces QR, rutas de ejercicios, TOC,
dimensiones, contraseña, fuentes usadas sin incrustar, transparencia residual,
resolución mínima, metadatos inconsistentes y artefactos generados preparados
para commit.

Reserva para revisión humana: legibilidad a escala impresa, ritmo de página,
calidad de imágenes escaladas, cobertura de tinta, texto comercial, categorías,
precio, derechos, ISBN, decisiones territoriales, cubierta y aprobación de la
prueba física.

## Método para el siguiente proyecto

1. Define lector, transformación prometida, formato y definición de “listo”.
2. Crea repositorio y journal persistente antes de escribir; registra decisiones,
   comandos, resultados, fallos y siguiente paso antes de cada commit.
3. Centraliza los metadatos y produce un capítulo piloto completo: prosa,
   actividad, evidencia, QR, sitio y PDF.
4. Convierte los patrones repetidos en manifiestos, generadores y validadores.
5. Construye un PDF de revisión desde el principio: el diseño cambia la escritura.
6. Congela una revisión, genera el PDF candidato, inspecciona el artefacto final
   y solicita una prueba.
7. Con el número final de páginas, crea cubierta usando la plantilla de la
   imprenta, coloca barcode en su área indicada y vuelve a probar.

## Checklist de entrega

- [ ] Una única fuente de prosa, manifest de recursos y metadatos centralizados.
- [ ] README con instalación, ruta de aprendizaje y explicación de QR.
- [ ] Sitio, QR, repositorio y PDF apuntan al mismo destino público estable.
- [ ] TOC generado desde el PDF final; sin números de página escritos a mano.
- [ ] Tamaño, márgenes, bleed, fuentes, imágenes y transparencias pasan preflight.
- [ ] Páginas críticas renderizadas e inspeccionadas; prueba física aprobada.
- [ ] Cubierta construida con la plantilla final y el número de páginas congelado.
- [ ] Journal, commit, manifiesto de publicación y archivo subido pertenecen a
      la misma revisión Git.

## La lección final

Un libro acompañado de repositorio no es un PDF con código extra. Es un sistema:
el libro da narrativa, el repositorio permite comprobar y extender, el sitio
reduce fricción y la imprenta exige disciplina en el artefacto final. Fuentes de
verdad compartidas, manifiestos y verificaciones hacen que ese sistema pueda
aplicarse a cualquier tema sin perder calidad ni confianza.
