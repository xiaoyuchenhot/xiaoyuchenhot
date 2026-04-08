import { motion } from 'framer-motion';

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.7, delay, ease: 'easeOut' },
});

export default function Hero() {
  return (
    <section
      id="home"
      className="relative min-h-screen flex items-center pt-24 pb-20 px-6 overflow-hidden"
      aria-label="Hero — Foodiez landing"
    >
      {/* Background ambient glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-orange-500/8 rounded-full blur-3xl pointer-events-none"
        aria-hidden="true"
      />
      <div
        className="absolute top-20 right-10 w-64 h-64 bg-orange-600/5 rounded-full blur-2xl pointer-events-none"
        aria-hidden="true"
      />

      <div className="max-w-6xl mx-auto w-full grid md:grid-cols-2 gap-16 items-center">
        {/* Text content */}
        <div>
          <motion.p
            {...fadeUp(0.1)}
            className="text-orange-500 font-semibold text-sm uppercase tracking-widest mb-5"
          >
            Fast. Fresh. Delivered.
          </motion.p>

          <motion.h1
            {...fadeUp(0.2)}
            className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.05] mb-6"
          >
            Food.{' '}
            <span className="text-orange-500">Fast.</span>
            <br />
            At Your Fingertips.
          </motion.h1>

          <motion.p
            {...fadeUp(0.35)}
            className="text-slate-400 text-lg leading-relaxed mb-10 max-w-md"
          >
            Order from hundreds of nearby restaurants and get it delivered to
            your door in minutes. No fuss, no waiting.
          </motion.p>

          <motion.div
            {...fadeUp(0.5)}
            className="flex flex-wrap gap-4"
          >
            <StoreButton
              href="#download"
              label="Download on the App Store"
              icon={<AppleIcon />}
              storeName="App Store"
              variant="light"
            />
            <StoreButton
              href="#download"
              label="Get Foodiez on Google Play"
              icon={<PlayIcon />}
              storeName="Google Play"
              variant="glass"
            />
          </motion.div>
        </div>

        {/* Phone mockup */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.9, delay: 0.3, ease: 'easeOut' }}
          className="hidden md:flex justify-center items-center"
          aria-hidden="true"
        >
          <PhoneMockup />
        </motion.div>
      </div>
    </section>
  );
}

interface StoreButtonProps {
  href: string;
  label: string;
  icon: React.ReactNode;
  storeName: string;
  variant: 'light' | 'glass';
}

function StoreButton({ href, label, icon, storeName, variant }: StoreButtonProps) {
  const base =
    'inline-flex items-center gap-3 font-semibold px-6 py-3.5 rounded-2xl transition-all duration-200 hover:scale-105 active:scale-95 min-h-[52px]';
  const styles =
    variant === 'light'
      ? 'bg-white text-slate-900 hover:bg-slate-100'
      : 'bg-white/10 text-white border border-white/20 hover:bg-white/20';

  return (
    <a href={href} className={`${base} ${styles}`} aria-label={label}>
      <span className="w-6 h-6 flex-shrink-0">{icon}</span>
      <span>{storeName}</span>
    </a>
  );
}

function AppleIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className="w-full h-full">
      <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
    </svg>
  );
}

function PlayIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className="w-full h-full">
      <path d="M3.18 23.76c.3.17.64.24.99.2L14.64 12 11 8.36 3.18 23.76zm17.12-9.5-2.93-1.67-3.64 3.64 3.64 3.64 2.96-1.69c.84-.48.84-1.64-.03-1.92zM2.15 1.02C2.06 1.2 2 1.4 2 1.62v20.76c0 .23.06.43.16.61L13.86 12 2.15 1.02zm11.35 10.24 3.54-3.54-10.02-5.71L7.02 2l10.48 11z" />
    </svg>
  );
}

function PhoneMockup() {
  const restaurants = [
    { name: 'Pizza Palace', time: '15 min', rating: '4.9', emoji: '🍕', gradient: 'from-red-500/30' },
    { name: 'Burger Town', time: '22 min', rating: '4.7', emoji: '🍔', gradient: 'from-yellow-500/30' },
    { name: 'Noodle House', time: '18 min', rating: '4.8', emoji: '🍜', gradient: 'from-orange-500/30' },
  ];

  return (
    <div className="relative w-72 h-[580px]">
      {/* Glow behind phone */}
      <div className="absolute inset-4 bg-orange-500/20 rounded-[3rem] blur-3xl" />
      {/* Phone shell */}
      <div className="relative w-full h-full bg-gradient-to-b from-slate-800 to-slate-900 rounded-[3rem] border border-white/10 overflow-hidden shadow-2xl flex flex-col">
        {/* Status bar */}
        <div className="relative h-10 bg-slate-900/80 flex items-center px-5 justify-between flex-shrink-0">
          <span className="text-white text-xs font-medium">9:41</span>
          <div className="absolute left-1/2 -translate-x-1/2 w-24 h-5 bg-black rounded-full" />
          <div className="flex gap-1 items-center">
            <div className="w-3 h-2 bg-white/50 rounded-sm" />
          </div>
        </div>

        {/* App content */}
        <div className="flex-1 bg-[#0F172A] p-4 flex flex-col gap-4 overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-xs">Good evening,</p>
              <p className="text-white font-bold text-base">What are you craving?</p>
            </div>
            <div className="w-8 h-8 rounded-full bg-orange-500/30 border border-orange-500/50 flex items-center justify-center">
              <span className="text-xs">👤</span>
            </div>
          </div>

          {/* Search bar */}
          <div className="bg-slate-800 rounded-xl px-3 py-2 flex items-center gap-2">
            <svg
              className="w-4 h-4 text-slate-400 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <span className="text-slate-400 text-xs">Search restaurants...</span>
          </div>

          {/* Categories */}
          <div className="flex gap-2 overflow-x-auto scrollbar-none">
            {['🍕 Pizza', '🍔 Burgers', '🍜 Noodles'].map((c) => (
              <span
                key={c}
                className="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300 whitespace-nowrap flex-shrink-0"
              >
                {c}
              </span>
            ))}
          </div>

          {/* Restaurant cards */}
          <div className="flex flex-col gap-3">
            {restaurants.map((r) => (
              <div
                key={r.name}
                className={`bg-gradient-to-r ${r.gradient} to-slate-800/80 rounded-2xl p-3 flex items-center justify-between border border-white/5`}
              >
                <div>
                  <p className="text-white text-sm font-semibold">{r.name}</p>
                  <p className="text-slate-400 text-xs">
                    {r.time} · ⭐ {r.rating}
                  </p>
                </div>
                <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-xl">
                  {r.emoji}
                </div>
              </div>
            ))}
          </div>

          {/* Bottom nav bar */}
          <div className="mt-auto bg-slate-800/80 rounded-2xl p-3 flex justify-around">
            {(['🏠', '🔍', '🛒', '👤'] as const).map((icon, i) => (
              <span
                key={i}
                className={`text-lg leading-none ${i === 0 ? 'opacity-100' : 'opacity-30'}`}
              >
                {icon}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
