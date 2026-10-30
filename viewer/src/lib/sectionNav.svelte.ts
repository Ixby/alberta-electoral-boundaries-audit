// Alberta Electoral Boundary Audit — in-page section navigation for the site header
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// A page with landmark sections (today only the main page) registers them here
// and keeps `current` in step with its scroll-spy. The site header shows the
// previous / current / next stepper and lists the sections in its drawer while
// `sections` is non-empty. The page clears it on destroy.

export type Section = { id: string; key: string };

export const sectionNav = $state<{ sections: Section[]; current: number }>({
	sections: [],
	current: 0
});
