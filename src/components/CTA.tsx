import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

function AppleIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className="w-6 h-6 flex-shrink-0">
      <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
    </svg>
  );
}

function PlayIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className="w-6 h-6 flex-shrink-0">
      <path d="M3.18 23.76c.3.17.64.24.99.2L14.64 12 11 8.36 3.18 23.76zm17.12-9.5-2.93-1.67-3.64 3.64 3.64 3.64 2.96-1.69c.84-.48.84-1.64-.03-1.92zM2.15 1.02C2.06 1.2 2 1.4 2 1.62v20.76c0 .23.06.43.16.61L13.86 12 2.15 1.02zm11.35 10.24 3.54-3.54-10.02-5.71L7.02 2l10.48 11z" />
    </svg>
  );
}

export default function CTA() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section
      id="download"
      ref={ref}
      className="py-28 px-6"
      aria-labelledby="cta-heading"
    >
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={inView ? { opacity: 1, scale: 1 } : {}}
          transition={{ duration: 0.7 }}
          className="relative bg-gradient-to-br from-orange-500/20 via-orange-600/10 to-transparent border border-orange-500/20 rounded-[3rem] p-14 md:p-20 overflow-hidden text-center"
        >
          {/* Decorative blurs */}
          <div
            className="absolute -top-24 -right-24 w-72 h-72 bg-orange-500/15 rounded-full blur-3xl pointer-events-none"
            aria-hidden="true"
          />
          <div
            className="absolute -bottom-24 -left-24 w-72 h-72 bg-orange-500/10 rounded-full blur-3xl pointer-events-none"
            aria-hidden="true"
          />

          <div className="relative z-10">
            <p className="text-orange-500 font-semibold text-sm uppercase tracking-widest mb-6">
              Get Started Today
            </p>
            <h2
              id="cta-heading"
              className="text-4xl md:text-6xl font-bold text-white tracking-tight leading-tight mb-6"
            >
              Hungry? Download
              <br />
              Foodiez now.
            </h2>
            <p className="text-slate-400 text-lg mb-10 max-w-md mx-auto leading-relaxed">
              Available on iOS and Android. Free to download — start ordering in
              under a minute.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="#"
                className="inline-flex items-center justify-center gap-3 bg-white text-slate-900 font-semibold px-8 py-4 rounded-2xl hover:bg-slate-100 hover:scale-105 active:scale-95 transition-all duration-200 min-h-[56px]"
                aria-label="Download Foodiez on the App Store"
              >
                <AppleIcon />
                <span>Download on App Store</span>
              </a>
              <a
                href="#"
                className="inline-flex items-center justify-center gap-3 bg-slate-800 text-white font-semibold px-8 py-4 rounded-2xl border border-white/10 hover:bg-slate-700 hover:scale-105 active:scale-95 transition-all duration-200 min-h-[56px]"
                aria-label="Get Foodiez on Google Play"
              >
                <PlayIcon />
                <span>Get it on Google Play</span>
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
