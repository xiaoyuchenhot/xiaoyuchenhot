import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const features = [
  {
    icon: '⚡',
    title: 'Fast Delivery',
    description:
      'Get your food delivered in minutes. We optimize every route so your meal arrives hot and fresh every time.',
  },
  {
    icon: '🍽️',
    title: 'Wide Selection',
    description:
      'Choose from hundreds of local restaurants across every cuisine. Something for every craving, every time.',
  },
  {
    icon: '📍',
    title: 'Real-Time Tracking',
    description:
      'Watch your order travel from kitchen to door on a live map. No more guessing when your food arrives.',
  },
  {
    icon: '💳',
    title: 'Easy Payments',
    description:
      'Secure, one-tap checkout with all major cards, Apple Pay, and Google Pay. No friction, just food.',
  },
  {
    icon: '🔒',
    title: 'Reliable Service',
    description:
      'Consistent, dependable delivery you can count on — every single order, every single time.',
  },
];

export default function Features() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section
      id="features"
      ref={ref}
      className="py-28 px-6"
      aria-labelledby="features-heading"
    >
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <p className="text-orange-500 font-semibold text-sm uppercase tracking-widest mb-4">
            Why Foodiez
          </p>
          <h2
            id="features-heading"
            className="text-4xl md:text-5xl font-bold text-white tracking-tight"
          >
            Everything you need.
            <br />
            Nothing you don&apos;t.
          </h2>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.article
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="group bg-white/5 hover:bg-white/10 border border-white/10 hover:border-orange-500/30 rounded-3xl p-8 backdrop-blur-sm transition-all duration-300 cursor-default"
            >
              <div
                className="text-4xl mb-5 select-none"
                role="img"
                aria-label={feature.title}
              >
                {feature.icon}
              </div>
              <h3 className="text-white font-bold text-xl mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.description}</p>
            </motion.article>
          ))}

          {/* CTA card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: features.length * 0.1 }}
            className="bg-gradient-to-br from-orange-500/20 to-orange-600/5 border border-orange-500/30 rounded-3xl p-8 flex flex-col justify-between"
          >
            <div>
              <p className="text-white font-bold text-xl mb-4">Ready to order?</p>
              <p className="text-slate-400 leading-relaxed mb-8">
                Join thousands of satisfied customers who trust Foodiez every day.
              </p>
            </div>
            <a
              href="#download"
              className="inline-flex justify-center items-center bg-orange-500 hover:bg-orange-400 text-white font-semibold px-6 py-3.5 rounded-2xl transition-all duration-200 hover:scale-105 active:scale-95 min-h-[48px]"
            >
              Get Started
            </a>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
