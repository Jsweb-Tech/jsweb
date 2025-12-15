# Forms

JsWeb provides a powerful and easy-to-use form library that simplifies the process of handling user input and validation.

## Creating a Form

To create a form, you can define a class that inherits from `jsweb.forms.Form`. You can then add fields to the form as class attributes.

```python
from jsweb.forms import Form, StringField, PasswordField, HiddenField
from jsweb.validators import DataRequired, Length, Email

class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    csrf_token = HiddenField()
```

## Form Fields

JsWeb provides a variety of form fields, including:

*   `StringField`
*   `PasswordField`
*   `BooleanField`
*   `IntegerField`
*   `FloatField`
*   `DateField`
*   `TimeField`
*   `DateTimeField`
*   `FileField`
*   `SelectField`
*   `RadioField`
*   `TextAreaField`
*   `HiddenField`

## Validators

Validators are used to check that the data submitted by the user is valid. You can pass a list of validators to a field's `validators` argument.

Some of the built-in validators include:

*   `DataRequired`: Checks that the field is not empty.
*   `Length`: Checks that the length of the input is within a certain range.
*   `Email`: Checks that the input is a valid email address.
*   `EqualTo`: Checks that the input is equal to the input of another field.
*   `NumberRange`: Checks that the input is within a certain number range.
*   `FileRequired`: Checks that a file has been uploaded.
*   `FileAllowed`: Checks that the uploaded file has an allowed extension.
*   `FileSize`: Checks that the uploaded file is within a certain size range.

## Rendering a Form

You can render a form in your templates by passing the form object to the `render` function.

```python
from jsweb.response import render
from .forms import LoginForm

@app.route("/login", methods=["GET", "POST"])
async def login(req):
    form = LoginForm(await req.form(), await req.files())
    if req.method == "POST" and form.validate():
        # Handle the login
        ...
    return render(req, "login.html", {"form": form})
```

In your template, you can then render the form fields individually.

```html
<!-- templates/login.html -->
<form method="post" enctype="multipart/form-data">
    {{ form.csrf_token() }}
    <div>
        {{ form.username.label }}
        {{ form.username() }}
        {% if form.username.errors %}
            <ul>
                {% for error in form.username.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    <div>
        {{ form.password.label }}
        {{ form.password() }}
        {% if form.password.errors %}
            <ul>
                {% for error in form.password.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    <button type="submit">Log In</button>
</form>
```
