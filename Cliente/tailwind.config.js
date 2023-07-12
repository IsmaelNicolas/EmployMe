/** @type {import('tailwindcss').Config} */

module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {}
	},
	plugins: [require('daisyui')],

	daisyui: {
		themes: [
			{
				mytheme: {
					primary: '#2B4162',
          secondary: '#FF1053',
          accent: '#4EA5D9',
          neutral: '#3DDC97',
          'base-100': '#FFFFFF',
				}
			},
			'light',
			'cupcake'
		]
	}
};
