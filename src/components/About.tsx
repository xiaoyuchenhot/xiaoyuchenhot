import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';

const stats = [
  { value: '500+', label: 'Local Restaurants' },
  { value: '~10 min', label: 'Average Delivery Time' },
  { value: '50K+', label: 'Happy Users' },
];

export default function About() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section
      id="about"
      ref={ref}
      className="py-28 px-6"
      aria-labelledby="about-heading"
    >
      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        {/* Text */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={inView ? { opacity: 1, x: 0 } : {}}
          transition={{ duration: 0.7 }}
        >
          <p className="text-orange-500 font-semibold text-sm uppercase tracking-widest mb-4">
            About Foodiez
          </p>
          <h2
            id="about-heading"
            className="text-4xl md:text-5xl font-bold text-white tracking-tight leading-tight mb-6"
          >
            Connecting you to
            <br />
            the food you love.
          </h2>
          <p className="text-slate-400 text-lg leading-relaxed mb-5">
            Foodiez was built for people who don't have time to wait. We partner
            with hundreds of local restaurants to bring you the best meals —
            fast, without compromising on quality or choice.
          </p>
          <p className="text-slate-400 text-lg leading-relaxed">
            Whether you're craving pizza at midnight or a healthy lunch during a
            work call, Foodiez has you covered every time.
          </p>
        </motion.div>

        {/* Stats */}
        <div className="flex flex-col gap-5">
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, x: 30 }}
              animate={inView ? { opacity: 1, x: 0 } : {}}
              transition={{ duration: 0.6, delay: i * 0.15 }}
              className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-sm"
            >
              <p className="text-5xl font-bold text-orange-500 mb-2" aria-label={stat.value}>
                {stat.value}
              </p>
              <p className="text-slate-400 text-lg">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
