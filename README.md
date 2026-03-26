# 🚀 PMS - Plataforma de Gestión Empresarial

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Un sistema de gestión (PMS) moderno, rápido y escalable desarrollado en **Python con Flask**. Diseñado con una arquitectura limpia basada en **Blueprints**, este sistema ofrece un panel de control intuitivo para la administración de clientes, productos, pedidos y perfiles de usuario.

---

## ✨ Características Principales

* **🔐 Autenticación Segura:** Sistema de Login y protección de rutas mediante decoradores personalizados (`@login_requerido`).
* **👤 Gestión de Usuarios:** Perfiles dinámicos con soporte para actualización de datos (nombre, edad, sexo) y avatares personalizados mediante URL.
* **📱 Interfaz UI/UX Moderna:** Diseño profesional y 100% responsivo construido con **Bootstrap 5**. Incluye un *Sidebar* lateral colapsable (Holy Grail Layout) que se adapta a cualquier pantalla.
* **⚙️ Arquitectura Escalable:** Estructura modular utilizando Flask Blueprints para separar la lógica de usuarios (`acciones_usuarios`), autenticación y vistas generales.
* **🗄️ Conexión a Base de Datos:** Integración estructurada con modelos de datos para operaciones CRUD eficientes.

---

## 📸 Capturas de Pantalla

| Panel de Control (Dashboard) | Perfil de Usuario |
|:---:|:---:|
| <img src="URL_DE_TU_IMAGEN_AQUI" width="400" alt="Dashboard"> | <img src="URL_DE_TU_IMAGEN_AQUI" width="400" alt="Perfil"> |

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado en tu máquina local:
* [Python 3.8+](https://www.python.org/downloads/)
* PIP (Gestor de paquetes de Python)
* Servidor de Base de Datos (ej. MySQL/XAMPP)

---

## 🚀 Instalación y Uso

Sigue estos pasos para correr el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/](https://github.com/)[Tu_Usuario]/[Tu_Repositorio].git
   cd [Tu_Repositorio]

2. **Crea tu entornio virtual**
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. **Instala las dependencias del proyecto (Con tu entorno virtual activo)**
pip install -r requirements.txt