# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Notes on assets, favicon and Vite watch loops

If you place files into `public/` or a synced folder (OneDrive/Dropbox) Vite may detect repeated external writes and trigger HMR reload loops. To avoid issues:

- Prefer importing frequently-changed or development-only assets from `src/assets` and let Vite bundle them. Example in React components:
	```jsx
	import logo from '../assets/favicon.svg'
	<img src={logo} />
	```

- Use `public/` for true static assets that are not modified by external processes during development. If an external process writes into `public/assets`, add an ignore rule in `vite.config.js`:
	```js
	export default defineConfig({
		server: { watch: { ignored: ['**/public/assets/**'] } }
	})
	```

- For favicon changes use a versioned filename or query string to bust browser cache, e.g. `<link rel="icon" href="/assets/favicon.png?v=2">`.

- If you still see reload loops, check for external sync processes (OneDrive/Dropbox), automated build scripts, or git hooks writing files into `public/` and stop them during development.

## Running frontend locally (recommended for development)

```powershell
cd pariwisata-recommender\frontend
npm install
npm run dev
```

If you run inside Docker, the container might restart or be stopped by environment resource limits; running locally avoids extra complexity while developing UI.
