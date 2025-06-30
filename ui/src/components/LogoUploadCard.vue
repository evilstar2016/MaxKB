<template>
  <div class="logo-upload-card">
    <el-card shadow="never" class="mb-8">
      <template #header>
        <div class="flex-between">
          <span class="card-title">{{ title }}</span>
          <el-upload
            ref="uploadRef"
            action="#"
            :auto-upload="false"
            :show-file-list="false"
            :accept="acceptTypes"
            :on-change="handleChange"
            :before-upload="beforeUpload"
          >
            <el-button size="small" type="primary">
              {{ $t('components.logoUpload.changeImage') }}
            </el-button>
          </el-upload>
        </div>
      </template>
      
      <div class="upload-content">
        <div class="preview-container" v-if="currentLogo">
          <img :src="currentLogo" :alt="title" class="logo-preview" />
        </div>
        <div class="empty-state" v-else>
          <el-icon class="empty-icon"><Picture /></el-icon>
          <p class="empty-text">{{ $t('components.logoUpload.uploadLogo') }}</p>
        </div>
        
        <div class="upload-info">
          <p class="recommend-size">
            {{ $t('components.logoUpload.recommendSize') }}: {{ recommendSize }}
          </p>
          <p class="description">{{ description }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { Picture } from '@element-plus/icons-vue'
import type { UploadFile, UploadFiles } from 'element-plus'
import { ElMessage } from 'element-plus'
import { t } from '@/locales'

defineOptions({
  name: 'LogoUploadCard'
})

interface Props {
  title: string
  logoType: 'header' | 'login' | 'favicon'
  currentLogo?: string
  modelValue?: File | string
}

const props = withDefaults(defineProps<Props>(), {
  currentLogo: '',
  modelValue: undefined
})

const emit = defineEmits<{
  'update:modelValue': [value: File | null]
  'change': [file: File | null, logoType: string]
}>()

const uploadRef = ref()

// 计算属性
const acceptTypes = computed(() => {
  return props.logoType === 'favicon' 
    ? 'image/jpeg,image/png,image/gif,image/svg+xml,image/x-icon'
    : 'image/jpeg,image/png,image/gif,image/svg+xml'
})

const recommendSize = computed(() => {
  const sizeMap = {
    header: '200×50px',
    login: '300×80px', 
    favicon: '32×32px'
  }
  return sizeMap[props.logoType] || '200×50px'
})

const description = computed(() => {
  const descMap = {
    header: t('components.logoUpload.headerLogoDesc'),
    login: t('components.logoUpload.loginLogoDesc'),
    favicon: t('components.logoUpload.faviconDesc')
  }
  return descMap[props.logoType] || ''
})

// 文件上传前验证
const beforeUpload = (file: UploadFile) => {
  const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/x-icon'].includes(file.type || '')
  const isValidSize = file.size! / 1024 / 1024 < 10

  if (!isValidType) {
    ElMessage.error(t('components.logoUpload.typeError'))
    return false
  }
  
  if (!isValidSize) {
    ElMessage.error(t('components.logoUpload.sizeError'))
    return false
  }

  return true
}

// 处理文件变化
const handleChange = (file: UploadFile, fileList: UploadFiles) => {
  if (!beforeUpload(file)) {
    return
  }

  emit('update:modelValue', file.raw || null)
  emit('change', file.raw || null, props.logoType)
}
</script>

<style lang="scss" scoped>
.logo-upload-card {
  .card-title {
    font-weight: 500;
    color: var(--el-text-color-primary);
  }

  .upload-content {
    .preview-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80px;
      margin-bottom: 16px;
      padding: 16px;
      border: 1px dashed var(--el-border-color-light);
      border-radius: 4px;
      background-color: var(--el-fill-color-lighter);

      .logo-preview {
        max-width: 100%;
        max-height: 60px;
        object-fit: contain;
      }
    }

    .empty-state {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      min-height: 80px;
      margin-bottom: 16px;
      padding: 16px;
      border: 1px dashed var(--el-border-color-light);
      border-radius: 4px;
      background-color: var(--el-fill-color-lighter);

      .empty-icon {
        font-size: 24px;
        color: var(--el-text-color-placeholder);
        margin-bottom: 8px;
      }

      .empty-text {
        margin: 0;
        color: var(--el-text-color-placeholder);
        font-size: 14px;
      }
    }

    .upload-info {
      .recommend-size {
        margin: 0 0 4px 0;
        font-size: 12px;
        color: var(--el-color-primary);
        font-weight: 500;
      }

      .description {
        margin: 0;
        font-size: 12px;
        color: var(--el-text-color-regular);
        line-height: 1.4;
      }
    }
  }
}
</style>