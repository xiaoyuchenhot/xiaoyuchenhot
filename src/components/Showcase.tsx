import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

interface ShowcaseItem {
  tag: string;
  heading: string;
  body: string;
  visual: string;
  visualLabel: string;
  bgGradient: string;
}

const items: ShowcaseItem[] = [
  {
    tag: 'Order in seconds',
    heading: 'Browse, tap, done.',
    body: 'Our interface is designed to get you from hungry to ordered in under 30 seconds. Browse menus, customize your order, and check out without ever leaving the app.',
    visual: '🍕',
    visualLabel: 'Pizza illustration representing fast ordering',
    bgGradient: 'from-red-500/20',
  },
  {
    tag: 'Always in the loop',
    heading: 'Watch it happen, live.',
    body: 'Real-time tracking puts you in control. See exactly where your rider is, and get notified the moment your food is ready and on its way.',
    visual: '📍',
    visualLabel: 'Map pin representing real-time tracking',
    bgGradient: 'from-blue-500/20',
  },
  {
    tag: 'Pay your way',
    heading: 'Checkout without the friction.',
    body: 'Saved cards, Apple Pay, Google Pay — pay however you prefer. Your data is encrypted and secure every step of the way.',
    visual: '💳',
    visualLabel: 'Credit card representing easy payments',
    bgGradient: 'from-green-500/20',
  },
];

function ShowcaseItem({ item, index }: { item: ShowcaseItem; index: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });
  const isEven = index % 2 === 0;

  return (
    <div ref={ref} className="grid md:grid-cols-2 gap-12 items-center">
      {/* Text — swaps order on odd rows */}
      <motion.div
        initial={{ opacity: 0, x: isEven ? -30 : 30 }}
        animate={inView ? { opacity: 1, x: 0 } : {}}
        transition={{ duration: 0.7 }}
        className={isEven ? '' : 'md:order-last'}
      >
        <p className="text-orange-500 font-semibold text-sm uppercase tracking-widest mb-4">
          {item.tag}
        </p>
        <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight leading-tight mb-5">
          {item.heading}
        </h2>
        <p className="text-slate-400 text-lg leading-relaxed">{item.body}</p>
      </motion.div>

      {/* Visual */}
      <motion.div
        initial={{ opacity: 0, x: isEven ? 30 : -30 }}
        animate={inView ? { opacity: 1, x: 0 } : {}}
        transition={{ duration: 0.7, delay: 0.15 }}
        className={`bg-gradient-to-br ${item.bgGradient} to-transparent rounded-3xl border border-white/10 h-64 flex items-center justify-center ${
          isEven ? '' : 'md:order-first'
        }`}
        role="img"
        aria-label={item.visualLabel}
      >
        <span className="text-9xl select-none" aria-hidden="true">
          {item.visual}
        </span>
      </motion.div>
    </div>
  );
}

export default function Showcase() {
  return (
    <section className="py-28 px-6" aria-label="Feature deep-dive">
      <div className="max-w-6xl mx-auto flex flex-col gap-24">
        {items.map((item, i) => (
          <ShowcaseItem key={item.tag} item={item} index={i} />
        ))}
      </div>
    </section>
  );
}
