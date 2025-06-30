<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin for <a href="https://ranger.fm/">Ranger</a>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
	<a href="https://github.com/catppuccin/template/stargazers"><img src="https://img.shields.io/github/stars/catppuccin/template?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
	<a href="https://github.com/catppuccin/template/issues"><img src="https://img.shields.io/github/issues/catppuccin/template?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
	<a href="https://github.com/catppuccin/template/contributors"><img src="https://img.shields.io/github/contributors/catppuccin/template?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/previews/preview.webp"/>
</p>

## Previews

<details>
<summary>🌻 Latte</summary>
<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/previews/latte.webp"/>
</details>
<details>
<summary>🪴 Frappé</summary>
<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/previews/frappe.webp"/>
</details>
<details>
<summary>🌺 Macchiato</summary>
<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/previews/macchiato.webp"/>
</details>
<details>
<summary>🌿 Mocha</summary>
<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/previews/mocha.webp"/>
</details>

## Usage

1. Go to the **Releases** page and download your preferred flavor(s).
2. Find your ranger colorschemes directory. Usually, it is located in
   `~/.config/ranger/colorschemes`. If you don't have a ~/.config/ranger
   directory:
   - Run `ranger --copy-config=(rc)`
   - Go to `~/.config/ranger` and create a directory called `colorschemes`.
3. Copy or link your downloaded colorscheme file(s) to your
   `~/.config/ranger/colorschemes` directory.
   - If you want to **copy**, run
     ```bash
     cp catppuccin_<flavor>.py ~/.config/ranger/colorschemes
     ```
   - If you want to **link**, run
     ```bash
     ln -s catppuccin_<flavor>.py ~/.config/ranger/colorschemes
     ```
4. Go to your `rc.conf` file located in `~/.config/ranger/rc.conf`.
5. Update the line `set colorscheme ...` to reference your flavor:
   ```diff
   # Which colorscheme to use?  These colorschemes are available by default:
   # default, jungle, snow, solarized
   - set colorscheme ...
   + set colorscheme catppuccin_mocha
   ```

## Building

If you want to customize the theme or contribute to it, you can clone the repo
and build the theme files for yourself.

Just run the build script to generate the theme files:

```bash
python3 build.py
```

This will generate the colorscheme files in the `./output` directory.

## 💝 Thanks to

- [dfrico](https://github.com/dfrico)
- [computergnome99](https://github.com/computergnome99)

&nbsp;

<p align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" />
</p>

<p align="center">
	Copyright &copy; 2021-present <a href="https://github.com/catppuccin" target="_blank">Catppuccin Org</a>
</p>

<p align="center">
	<a href="https://github.com/catppuccin/catppuccin/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
