# Arcticons-selfhosted - Arcticons for self-hosted dashboards!


**NOTICE: this is an unofficial WIP. I'll probably showcase this to Arcticons-team later, when I have the time to, but for now it stays here as demo.**

<center>
| Website | Matrix Chat (Arcticons Space) | Knowledge Base |
</center>

## Usage

See website to search for icons, or search directly on this Github repo.

## Contribute

To contribute icons:

1. Add them to the `/newicons` folder in a pull request.

    - Icons shall follow [contribution guidelines](https://docs.arcticons.com/contribute/creating-icons) and the [Knowledge Base](https://docs.arcticons.com) tutorials.
    - Please name icons with underscores as spaces (e.g. `jitsi_meet.svg`) so they can be titled properly (`Jitsi Meet`).


2. Assign a category for them in `/newicons/appfilter.json`. The current categories are:
    - **selfhosted**: Selfhosted software
    - **programming**: Programming tools and languages
    - **distros**: Linux distributions and other OSes
    - **other**: Miscellaneous stuff related to self-hosting e.g. logos of popular services or utility icons

<details>
<summary>Extra tips</summary>

- A lot of icons may already exist in the [main Android repo](https://github.com/Arcticons-team/Arcticons), you can copy-paste and categorise them accordingly
- To avoid cloning the huge `/icons` folder, you can clone use [git sparse-checkout](https://stackoverflow.com/a/63786181) with the `/newicons` folder:
  
    ```bash
    git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/Arcticons-team/Arcticons-selfhosted
    cd Arcticons-selfhosted
    git sparse-checkout add newicons
    git checkout
    ```

</details>

## Requests and issues

Please file an issue, preferably with link(s) to the logo(s).

## Credits

Inspiration from https://selfh.st/icons.

Thank you to all contributors!

## License

Arcticons-selfhosted uses the [GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

All icons are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).