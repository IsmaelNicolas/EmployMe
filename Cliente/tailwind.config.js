/** @type {import('tailwindcss').Config} */

export const content = ['./src/**/*.{html,js,svelte,ts}'];
export const theme = {
	extend: {}
};
export const plugins = [require('daisyui')];
export const daisyui = {
	themes: [
		{
			mytheme: {
				primary: '#2B4162',
				secondary: '#FF1053',
				accent: '#4EA5D9',
				neutral: '#3DDC97',
				'base-100': '#FFFFFF'
			}
		},
		'light',
		'cupcake'
	]
};
