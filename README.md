# Online Course Application — Django Final Project

Aplicación de curso en línea desarrollada con Django 4.x que implementa el módulo
de exámenes (modelos `Question`, `Choice` y `Submission`), vistas de envío y
resultados, panel de administración con inlines y plantillas con Bootstrap 5.

## Características
- Modelos: `Course`, `Lesson`, `Instructor`, `Learner`, `Enrollment`, `Question`, `Choice`, `Submission`.
- Panel de administración con `QuestionInline`, `ChoiceInline`, `QuestionAdmin` y `LessonAdmin`.
- Examen con preguntas de opción múltiple y calificación automática.
- Vistas `submit` y `show_exam_result` con protección `@login_required`.
- Plantillas responsivas con Bootstrap 5.

## Cómo ejecutarlo
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver