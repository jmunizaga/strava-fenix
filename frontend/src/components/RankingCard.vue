<template>
  <div class="card card-hover p-5 mb-4 border-l-4 border-fenix-orange group">
    <div class="flex items-center gap-4">
      <!-- Rank Badge -->
      <div class="flex-shrink-0">
        <div 
          class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg"
          :class="rankBadgeClass"
        >
          {{ rank }}
        </div>
      </div>

      <!-- Athlete Info -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-3 mb-2">
          <img 
            v-if="athlete.profile"
            :src="athlete.profile" 
            :alt="athleteName"
            class="w-12 h-12 rounded-full object-cover border-2 border-fenix-orange shadow-md"
          />
          <div 
            v-else
            class="w-12 h-12 rounded-full bg-fenix-black flex items-center justify-center text-white font-black text-sm border-2 border-fenix-orange shadow-md"
          >
            {{ initials }}
          </div>
          <div class="min-w-0">
            <h3 class="font-black text-lg text-fenix-black truncate uppercase tracking-tight group-hover:text-fenix-orange transition-colors">{{ athleteName }}</h3>
            <p class="text-[10px] font-bold text-fenix-gray-500 uppercase tracking-[0.15em]">{{ metrics.activities_count }} sesiones de entrenamiento</p>
          </div>
        </div>

        <!-- Metrics -->
        <div class="grid grid-cols-3 gap-2">
          <MetricBadge 
            icon="🚴"
            label="Distancia"
            :value="metrics.total_distance / 1000"
            unit="km"
            :decimals="1"
          />
          <MetricBadge 
            icon="⛰️"
            label="Elevación"
            :value="metrics.total_elevation"
            unit="m"
            :decimals="0"
          />
          <MetricBadge 
            icon="🏆"
            label="Más largo"
            :value="metrics.longest_ride / 1000"
            unit="km"
            :decimals="1"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MetricBadge from './MetricBadge.vue';

export default {
  name: 'RankingCard',
  components: {
    MetricBadge
  },
  props: {
    rank: {
      type: Number,
      required: true
    },
    athlete: {
      type: Object,
      required: true
    },
    metrics: {
      type: Object,
      required: true
    }
  },
  computed: {
    athleteName() {
      return `${this.athlete.firstname} ${this.athlete.lastname}`;
    },
    initials() {
      return `${this.athlete.firstname[0]}${this.athlete.lastname[0]}`.toUpperCase();
    },
    rankBadgeClass() {
      if (this.rank === 1) {
        return 'bg-gradient-to-br from-yellow-400 to-yellow-600 text-white';
      } else if (this.rank === 2) {
        return 'bg-gradient-to-br from-gray-300 to-gray-500 text-white';
      } else if (this.rank === 3) {
        return 'bg-gradient-to-br from-orange-400 to-orange-600 text-white';
      }
      return 'bg-fenix-gray-200 text-fenix-gray-600';
    }
  }
}
</script>
