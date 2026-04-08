const companyLinks = ['About', 'Careers', 'Blog', 'Press'];
const legalLinks = ['Privacy Policy', 'Terms of Service', 'Cookie Policy'];

const socialLinks = [
  {
    label: 'Twitter / X',
    path: 'M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z',
  },
  {
    label: 'Instagram',
    path: 'M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37zm1.5-4.87h.01M7.5 20.5h9a6 6 0 006-6v-9a6 6 0 00-6-6h-9a6 6 0 00-6 6v9a6 6 0 006 6z',
  },
  {
    label: 'Facebook',
    path: 'M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z',
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-white/10 py-14 px-6" role="contentinfo">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <p className="text-2xl font-bold mb-4 select-none">
              <span className="text-white">Food</span>
              <span className="text-orange-500">iez</span>
            </p>
            <p className="text-slate-400 text-sm leading-relaxed max-w-xs">
              Fast, fresh food delivered to your door. Available on iOS and
              Android. Order smarter, eat better.
            </p>
          </div>

          {/* Company links */}
          <nav aria-label="Company links">
            <h3 className="text-white font-semibold mb-4 text-sm">Company</h3>
            <ul className="flex flex-col gap-3">
              {companyLinks.map((link) => (
                <li key={link}>
                  <a
                    href="#"
                    className="text-slate-400 hover:text-white text-sm transition-colors duration-200"
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          {/* Legal links */}
          <nav aria-label="Legal links">
            <h3 className="text-white font-semibold mb-4 text-sm">Legal</h3>
            <ul className="flex flex-col gap-3">
              {legalLinks.map((link) => (
                <li key={link}>
                  <a
                    href="#"
                    className="text-slate-400 hover:text-white text-sm transition-colors duration-200"
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-slate-500 text-sm">
            &copy; {new Date().getFullYear()} Foodiez. All rights reserved.
          </p>
          <div className="flex gap-5">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href="#"
                className="text-slate-400 hover:text-white transition-colors duration-200 min-w-[44px] min-h-[44px] flex items-center justify-center"
                aria-label={social.label}
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  strokeWidth={2}
                  aria-hidden="true"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d={social.path} />
                </svg>
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
