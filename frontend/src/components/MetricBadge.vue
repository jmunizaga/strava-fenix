<template>
  <div class="metric-badge inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-strava-gray-100 text-strava-gray-700">
    <span class="text-xl">{{ icon }}</span>
    <div class="flex flex-col">
      <span class="text-xs font-medium text-strava-gray-500 uppercase">{{ label }}</span>
      <span class="text-sm font-semibold">{{ formattedValue }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MetricBadge',
  props: {
    icon: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    value: {
      type: Number,
      required: true
    },
    unit: {
      type: String,
      default: ''
    },
    decimals: {
      type: Number,
      default: 1
    }
  },
  computed: {
    formattedValue() {
      const val = this.value.toFixed(this.decimals);
      return `${val} ${this.unit}`;
    }
  }
}
</script>
