<template>
  <div class="min-h-screen pb-6">
    <!-- Header -->
    <header class="bg-fenix-black shadow-lg sticky top-0 z-10 border-b-2 border-fenix-orange">
      <div class="max-w-2xl mx-auto px-4 py-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center border-2 border-fenix-orange shadow-inner">
              <span class="text-2xl">🔥</span>
            </div>
            <div>
              <h1 class="text-2xl font-black text-white tracking-tight uppercase">Fénix <span class="text-fenix-orange">Chile</span></h1>
              <p class="text-xs text-fenix-gray-400 font-bold uppercase tracking-widest">Ranking / {{ weekRange }}</p>
            </div>
          </div>
          
          <button 
            @click="loginWithStrava" 
            class="hidden sm:flex items-center gap-2 bg-fenix-orange text-white px-4 py-2 rounded-full font-black text-[10px] uppercase tracking-tighter hover:scale-105 transition-transform shadow-lg"
            :disabled="loading"
          >
            <span>Connect</span>
            <span class="bg-black text-white px-1.5 py-0.5 rounded-full">STRAVA</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Auth CTA -->
    <div class="sm:hidden p-4">
      <button 
        @click="loginWithStrava" 
        class="w-full flex items-center justify-center gap-2 bg-fenix-orange text-white py-3 rounded-xl font-black text-xs uppercase tracking-tight shadow-md"
        :disabled="loading"
      >
        <span>Connect with</span>
        <span class="bg-black text-white px-2 py-0.5 rounded-full">STRAVA</span>
      </button>
    </div>

    <!-- Filters -->
    <div class="max-w-2xl mx-auto px-4 py-4">
      <FilterTabs
        :selected-gender="selectedGender"
        @update:gender="selectedGender = $event"
      />
    </div>

    <!-- Rankings List -->
    <div class="max-w-2xl mx-auto px-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-12 h-12 border-4 border-fenix-orange border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-4 text-fenix-gray-600 font-bold uppercase text-xs tracking-widest">Sincronizando...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <span class="text-5xl mb-4 block">⚠️</span>
        <p class="text-fenix-gray-700 font-bold uppercase text-sm tracking-wide">{{ error }}</p>
        <button @click="fetchRankings" class="btn-primary mt-6">
          Reintentar
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="rankings.length === 0" class="text-center py-12 px-6">
        <span class="text-5xl mb-6 block">🏁</span>
        <p class="text-fenix-black font-black uppercase tracking-widest">No hay registros</p>
        <p class="text-fenix-gray-500 text-xs mt-3 font-bold uppercase tracking-tight">¡Sé el primero en salir a pedalear!</p>
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
          selectedGender.value,
          -1
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

    const loginWithStrava = async () => {
      try {
        const url = await rankingsApi.getLoginUrl();
        window.location.href = url;
      } catch (err) {
        console.error('Error getting login URL:', err);
        error.value = 'No se pudo iniciar la conexión con Strava.';
      }
    };

    const handleCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      
      if (code) {
        loading.value = true;
        try {
          await rankingsApi.sendAuthCallback(code);
          // Clean URL
          window.history.replaceState({}, document.title, window.location.pathname);
          // Refresh rankings
          await fetchRankings();
          alert('¡Conectado con éxito! Tus datos ahora aparecerán en el ranking.');
        } catch (err) {
          console.error('Error in auth callback:', err);
          error.value = 'Error al autorizar con Strava.';
        } finally {
          loading.value = false;
        }
      }
    };

    // Watch for filter changes
    watch([selectedGender], () => {
      fetchRankings();
    });

    // Initial load
    onMounted(async () => {
      await handleCallback();
      fetchRankings();
    });

    return {
      loading,
      error,
      rankings,
      selectedGender,
      weekRange,
      fetchRankings,
      loginWithStrava
    };
  }
}
</script>
