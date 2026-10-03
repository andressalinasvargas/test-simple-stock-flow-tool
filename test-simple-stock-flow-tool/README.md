# test-simple-stock-flow-tool

> **Prueba técnica · Ficha ADSO 3413974**
> Horario: de **9:00 a. m. a 3:00 p. m.** (15:00)

Este repositorio guarda las **utilidades** de *Simple Stock Flow*: el sembrador de datos de demostración, que usa la API. **Empieza vacío a propósito**: se construye en el fork de cada aprendiz.

## Instrucciones

Cada aprendiz debe **crear el fork** de los seis repositorios del proyecto y **resolver el proyecto
con el spec planteado**.

1. Hacer fork, a su cuenta de GitHub, de cada repositorio de la tabla del final.
2. Leer el spec en [`test-simple-stock-flow-docs`](https://github.com/code-sena/test-simple-stock-flow-docs).
   Se entrega en dos versiones: `spec-python/` y `spec-.net/`.
3. Desarrollar en los forks.

## El reto se desarrolla con React y PHP (Laravel)

El spec está escrito para Python y para .NET, pero el reto **no** se hace en esos lenguajes:

| Capa | Tecnología del reto |
|---|---|
| Frontend | React |
| Backend | PHP con Laravel |

Lo que el spec define sobre el negocio —historias, criterios de aceptación, reglas, contrato de la
API, modelo de datos— se respeta. Lo que define sobre la tecnología se traduce a React y Laravel.

## La prueba no consiste en escribir el código

El propósito principal es ver la **capacidad de desempeño con SDD** (*Spec-Driven Development*,
desarrollo guiado por especificación): cómo se lee, se interpreta y se aplica una especificación
para llevarla a un stack distinto. El código es el medio, no el fin.

## Los seis repositorios

| Repositorio | Qué va ahí |
|---|---|
| [`test-simple-stock-flow-docs`](https://github.com/code-sena/test-simple-stock-flow-docs) | El spec: `spec-python/` y `spec-.net/` |
| [`test-simple-stock-flow-api`](https://github.com/code-sena/test-simple-stock-flow-api) | Backend en PHP (Laravel) |
| [`test-simple-stock-flow-app`](https://github.com/code-sena/test-simple-stock-flow-app) | Frontend en React |
| [`test-simple-stock-flow-page`](https://github.com/code-sena/test-simple-stock-flow-page) | Sitio público estático de presentación |
| [`test-simple-stock-flow-infra`](https://github.com/code-sena/test-simple-stock-flow-infra) | Contenedores, red, volúmenes y motor de base de datos vacío |
| [`test-simple-stock-flow-tool`](https://github.com/code-sena/test-simple-stock-flow-tool) | Utilidades: sembrador de datos de demostración |
