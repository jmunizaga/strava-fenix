<template>
  <div class="min-h-screen pb-6">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-2xl mx-auto px-4 py-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-strava-orange rounded-lg flex items-center justify-center">
            <span class="text-2xl">🚴</span>
          </div>
          <div>
            <h1 class="text-xl font-bold text-strava-gray-900">Fenix Rankings</h1>
            <p class="text-xs text-strava-gray-500">Semana del {{ weekRange }}</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Filters -->
    <div class="max-w-2xl mx-auto px-4 py-4">
      <FilterTabs
        :selected-gender="selectedGender"
        :selected-category="selectedCategory"
        @update:gender="selectedGender = $event"
        @update:category="selectedCategory = $event"
      />
    </div>

    <!-- Rankings List -->
    <div class="max-w-2xl mx-auto px-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-12 h-12 border-4 border-strava-orange border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-4 text-strava-gray-600">Cargando rankings...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <span class="text-5xl mb-4 block">⚠️</span>
        <p class="text-strava-gray-700 font-medium">{{ error }}</p>
        <button @click="fetchRankings" class="btn-primary mt-4">
          Reintentar
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="rankings.length === 0" class="text-center py-12">
        <span class="text-5xl mb-4 block">🏁</span>
        <p class="text-strava-gray-700 font-medium">No hay actividades esta semana</p>
        <p class="text-strava-gray-500 text-sm mt-2">¡Sal a pedalear!</p>
      </div>

      <!-- Rankings -->
      <div v-else>
        <RankingCard
          v-for="(item, index) in rankings"
          :key="item.athlete.id"
          :rank="index + 1"
          :athlete="item.athlete"
          :metrics="item"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue';
import FilterTabs from '../components/FilterTabs.vue';
import RankingCard from '../components/RankingCard.vue';
import { rankingsApi } from '../services/api';

export default {
  name: 'RankingView',
  components: {
    FilterTabs,
    RankingCard
  },
  setup() {
    const loading = ref(false);
    const error = ref(null);
    const rankings = ref([]);
    const selectedGender = ref(null);
    const selectedCategory = ref('general');
    const weekStart = ref(null);
    const weekEnd = ref(null);

    const weekRange = computed(() => {
      if (!weekStart.value || !weekEnd.value) return '';
      
      const start = new Date(weekStart.value);
      const end = new Date(weekEnd.value);
      
      const formatDate = (date) => {
        return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
      };
      
      return `${formatDate(start)} - ${formatDate(end)}`;
    });

    const fetchRankings = async () => {
      loading.value = true;
      error.value = null;
      
      try {
        const data = await rankingsApi.getWeeklyRankings(
          selectedCategory.value,
          selectedGender.value,
          0
        );
        
        rankings.value = data.rankings;
        weekStart.value = data.week_start;
        weekEnd.value = data.week_end;
      } catch (err) {
        console.error('Error fetching rankings:', err);
        error.value = 'Error al cargar los rankings. Verifica la conexión con el servidor.';
      } finally {
        loading.value = false;
      }
    };

    // Watch for filter changes
    watch([selectedGender, selectedCategory], () => {
      fetchRankings();
    });

    // Initial load
    onMounted(() => {
      fetchRankings();
    });

    return {
      loading,
      error,
      rankings,
      selectedGender,
      selectedCategory,
      weekRange,
      fetchRankings
    };
  }
}
</script>
