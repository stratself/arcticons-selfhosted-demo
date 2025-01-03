# Contributing


## To contribute icons

1. Clone the repository
2. Create the icons following the [contribution guidelines](https://docs.arcticons.com/contribute/creating-icons) and [Knowledge Base](https://docs.arcticons.com) tutorials.
3. Add them to the `/newicons` folder.
    - Please name icons with underscores as spaces (e.g. `jitsi_meet.svg`) so they can be titled properly (`Jitsi Meet`).
4. Assign a category for them in `/newicons/appfilter.json`. The current categories are:
    - **selfhosted**: Selfhosted software
    - **programming**: Programming tools and languages
    - **distros**: Linux distributions and other OSes
    - **other**: Miscellaneous stuff related to self-hosting e.g. logos of popular services or utility icons
4. If the icon is an _alternative_ logo of another icon, add them in the `"alts"` field.
5. Create a pull request and it'll be merged after some reviewing!

## Other ways to contribute

- Add/re-edit categories and alts `/newicons/appfilter.json` when something's not right
- Report problems in the issue tracker


<details>
<summary>Extra tips</summary>

- A lot of icons may already exist in the [main Android repo](https://github.com/Arcticons-team/Arcticons), you can copy-paste and categorise them accordingly
- To avoid cloning the entire huge repo, you can use [git sparse-checkout](https://stackoverflow.com/a/63786181) with the `/newicons` folder only:
  
    ```bash
    git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/Arcticons-team/Arcticons-selfhosted
    cd Arcticons-selfhosted
    git sparse-checkout add newicons
    git checkout
    ```

</details>
