<div align="center">
  <img alt="Autonomix" src="/res/logo.png" width="200px" />
  <h1>Autonomix</h1>
  <p> Odoo Hackathon 2024 project</p>
  <p><italic>Made by Romain Croughs, Lucas Van Praag, Oleksandra Omelyanyuk & Kamila Mortel</italic></p>
</div>

---

Automomix is a project developed, in a 48-hour period, during the Odoo Hackathon 2024. The subject of the hackathon was *"UI without text"*. Autonomix is a suite of tools that aims to help people with illiteracy to use a computer. The project is composed of four tools:

- **Recipes**: A tool that helps people to follow a recipe by showing them the steps to follow.
- **Agenda/Todo List**: Displaying the tasks to do during the day without any text.
- **Shopping list**: Create a shopping list without any text.
- **Contacts**: Displaying the contacts with their pictures.

Exclusively written in Python, the backend uses Flask and SQLite3, the frontend uses GTK4.

## Dependencies

To run the project you need to have the following packages installed:

- `GTK4` (See [GTK4 Installation for Python](https://gnome.pages.gitlab.gnome.org/pygobject/getting_started.html))
- `Python 3`

All the dependencies are listed in the `pyproject.toml` file. You can install them by running the following command:

```bash
pip install .
```

or using `uv`:

```bash
uv sync
```

## Licence

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
