<template>
  <div class="card card-hover p-4 mb-3">
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
            class="w-10 h-10 rounded-full object-cover border-2 border-strava-gray-200"
          />
          <div 
            v-else
            class="w-10 h-10 rounded-full bg-strava-gray-300 flex items-center justify-center text-white font-semibold"
          >
            {{ initials }}
          </div>
          <div class="min-w-0">
            <h3 class="font-semibold text-base text-strava-gray-900 truncate">{{ athleteName }}</h3>
            <p class="text-xs text-strava-gray-500">{{ metrics.activities_count }} actividades</p>
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
      return 'bg-strava-gray-200 text-strava-gray-700';
    }
  }
}
</script>
