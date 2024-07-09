## LFTplatform

LFTplatform is a Django-based platform designed to facilitate management of guilds and their teams in MMO projects.
It allows users to create, update, and manage **guilds**, **teams**, **characters**, and recruitment with additional functionality for filtering and searching based on various criteria.


Project was commissioned by one of the largest European MMO gaming communities and is currently undergoing active testing. It aims to streamline and unify the recruitment process, moving it from Discord channels to a structured and organized platform. Recruiters can create guilds, provide all relevant links, add teams, specify activity times, and indicate the types of players they are looking for. Players searching for a guild can filter existing guilds and choose the one that suits them best.

This project is primarily aimed at owners of MMO Discord community servers.
### Features


- **Guild Management**: Create and manage guilds, including administrative tools.
- **Team Management**: Organize teams within guilds, with roles and permissions.

- **Recruitment Tools**: Easily manage and track recruits across guilds and teams.
- **Character Management**: Manage player characters, including details and specs.
- **Advanced Filtering Options**: Filter guilds and teams by faction, activity times, team size, loot system, classes, and specific specs.

### Discord Integration

LFTplatform includes integration with Discord for authentication and authorization purposes:
- Use Discord OAuth2 for user/recruiter authentication.
- Enable Discord authorization for a seamless login experience.
- Extend community engagement with integrated Discord features.
- Check user roles on Discord servers for specific permissions (e.g., recruiter or recruit).

### Setup

To set up and run the project locally:
1. Clone this repository.
2. Install dependencies listed in `requirements.txt`:
    `
    pip install -r requirements.txt
    `
3. Configure your database settings in `settings.py`.
4. Create a `.env` file in the root directory of your project and add the following variables:
    ```env
    GENERATED_URL = "https://discord.com/oauth2/authorize?client_id="
    REDIRECT_URI = "/accounts/login/discord/authorization"
    API_ENDPOINT = "https://discord.com/api/v10"
    CLIENT_ID = your client id
    CLIENT_SECRET = your client secret
    PWV_SERVER_ID = community server id
    RECRUITER_ROLE_ID = server role ID, who has enough rights for recruiting
    ```
5. Make migrations:
    `
    python manage.py makemigrations
    `
6. Apply migrations:
    `
    python manage.py migrate
    `
7. Create a superuser:
    `
    python manage.py createsuperuser
    `
8. Start the development server:
    `
    python manage.py runserver
    `

### Usage

- Navigate to `/admin` to access the admin interface.
- Use the provided views and forms to manage characters, guilds, and teams.
- Utilize filtering options in the guild list view to find specific guilds based on criteria such as faction, activity times, raid size, loot system, classes, and specific specs.

### Customization

LFTplatform is designed with flexibility in mind, making it _easy to customize for other MMO projects_. The core social models (guild -> team -> recruit) can be adapted to fit the structure of other MMOs with similar organizational needs.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Support

For questions about setup or customization, contact: serhiienko.b.i@gmail.com
