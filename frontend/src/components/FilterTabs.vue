<template>
  <div class="filter-tabs">
    <div class="mb-4">
      <h3 class="text-sm font-medium text-strava-gray-600 mb-2 uppercase tracking-wide">Género</h3>
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="option in genderOptions"
          :key="option.value"
          @click="$emit('update:gender', option.value)"
          class="tab-button"
          :class="selectedGender === option.value ? 'tab-active' : 'tab-inactive'"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <div>
      <h3 class="text-sm font-medium text-strava-gray-600 mb-2 uppercase tracking-wide">Categoría</h3>
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="option in categoryOptions"
          :key="option.value"
          @click="$emit('update:category', option.value)"
          class="tab-button text-sm"
          :class="selectedCategory === option.value ? 'tab-active' : 'tab-inactive'"
        >
          {{ option.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FilterTabs',
  props: {
    selectedGender: {
      type: String,
      default: null
    },
    selectedCategory: {
      type: String,
      default: 'general'
    }
  },
  emits: ['update:gender', 'update:category'],
  data() {
    return {
      genderOptions: [
        { value: null, label: 'Todos' },
        { value: 'M', label: 'Hombres' },
        { value: 'F', label: 'Mujeres' }
      ],
      categoryOptions: [
        { value: 'general', label: 'General' },
        { value: 'elite', label: 'Elite' },
        { value: 'amateur', label: 'Amateur' },
        { value: 'master_a', label: 'Master A' },
        { value: 'master_b', label: 'Master B' },
        { value: 'master_c', label: 'Master C' },
        { value: 'master_d', label: 'Master D' }
      ]
    }
  }
}
</script>
