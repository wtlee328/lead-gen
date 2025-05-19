<template>
  <div class="engagement-center-wrapper">
    <!-- Header/Title for the View -->
    <header class="view-header p-3 border-bottom">
      <h3 class="m-0">{{ texts.engagementCenterTitle || 'Engagement Hub' }}</h3>
      <!-- Maybe some high-level stats or quick actions here -->
    </header>

    <div class="engagement-main-content">
      <!-- Left Pane: Lead Queue / List -->
      <aside class="lead-queue-sidebar border-end">
        <div class="p-3 border-bottom">
          <input
            type="text"
            class="form-control form-control-sm"
            :placeholder="texts.searchLeadsPlaceholder || 'Search leads in hub...'"
            v-model="searchQuery"
          />
          <div class="d-flex mt-2">
            <select class="form-select form-select-sm me-2" v-model="filterStatus">
              <option value="">{{ texts.filterByStatusAll || 'All Statuses' }}</option>
              <option value="pending_icebreaker">{{ texts.filterStatusPendingIcebreaker || 'Pending Icebreaker' }}</option>
              <option value="icebreaker_sent">{{ texts.filterStatusIcebreakerSent || 'Icebreaker Sent' }}</option>
              <option value="replied">{{ texts.filterStatusReplied || 'Replied' }}</option>
              <option value="follow_up_due">{{ texts.filterStatusFollowUpDue || 'Follow-up Due' }}</option>
            </select>
            <!-- Add more filters/sorts if needed -->
          </div>
        </div>

        <div class="lead-list-items scrollable-area">
          <div
            v-if="isLoading"
            class="text-center p-3 text-muted"
          >
            <div class="spinner-border spinner-border-sm" role="status"></div>
            <span class="ms-2">{{ texts.loading || 'Loading...' }}</span>
          </div>
          <ul v-else-if="filteredLeads.length > 0" class="list-group list-group-flush">
            <li
              v-for="lead in filteredLeads"
              :key="lead.id"
              class="list-group-item list-group-item-action"
              :class="{ active: selectedLead && selectedLead.id === lead.id }"
              @click="selectLead(lead)"
            >
              <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">{{ lead.name || `${lead.first_name} ${lead.last_name}`.trim() }}</h6>
                <small class="text-muted">{{ lead.icebreaker_status_display || getStatusDisplay(lead.icebreaker_status) }}</small>
              </div>
              <p class="mb-1 small text-muted">{{ lead.job_title }} at {{ lead.company_name }}</p>
              <small v-if="lead.next_follow_up_date" class="text-primary">
                <i class="bi bi-calendar-event"></i> {{ texts.followUpOn || 'Follow-up:' }} {{ formatDate(lead.next_follow_up_date) }}
              </small>
            </li>
          </ul>
          <div v-else class="text-center p-3 text-muted">
            {{ texts.noLeadsInHub || 'No leads in the hub matching your criteria.' }} <br>
            <small>{{ texts.addLeadsFromProspects || 'Add leads from the Prospects view.' }}</small>
          </div>
        </div>
      </aside>

      <!-- Right Pane: Selected Lead Workspace -->
      <main class="selected-lead-workspace p-3 scrollable-area">
        <div v-if="!selectedLead" class="text-center text-muted mt-5">
          <i class="bi bi-cursor-fill display-4"></i>
          <p class="lead mt-3">{{ texts.selectLeadPrompt || 'Select a lead from the list to start managing engagement.' }}</p>
        </div>

        <div v-if="selectedLead" class="lead-details-and-actions">
          <!-- Lead Header -->
          <div class="d-flex align-items-center mb-3 pb-3 border-bottom">
            <!-- <img :src="selectedLead.avatar_url || '/default_avatar.png'" alt="Avatar" class="rounded-circle me-3" width="60" height="60"> -->
            <div>
              <h4 class="mb-0">{{ selectedLead.name || `${selectedLead.first_name} ${selectedLead.last_name}`.trim() }}</h4>
              <p class="mb-0 text-muted">{{ selectedLead.job_title }} at {{ selectedLead.company_name }}</p>
              <a :href="selectedLead.linkedIn_url" target="_blank" class="small" v-if="selectedLead.linkedIn_url">
                <i class="bi bi-linkedin"></i> {{ texts.viewLinkedIn || 'View LinkedIn' }}
              </a>
            </div>
            <div class="ms-auto">
              <button @click="removeFromHub(selectedLead)" class="btn btn-sm btn-outline-danger">
                <i class="bi bi-x-circle"></i> {{ texts.removeFromHub || 'Remove from Hub' }}
              </button>
            </div>
          </div>

          <!-- Icebreaker Section -->
          <div class="card mb-3">
            <div class="card-header d-flex justify-content-between align-items-center">
              <span>{{ texts.icebreakerSectionTitle || 'Icebreaker Message' }}</span>
              <span :class="`badge bg-${getIcebreakerStatusClass(selectedLead.icebreaker_status)}`">
                {{ selectedLead.icebreaker_status_display || getStatusDisplay(selectedLead.icebreaker_status) }}
              </span>
            </div>
            <div class="card-body">
              <textarea
                class="form-control mb-2"
                rows="5"
                v-model="currentIcebreakerMessage"
                :placeholder="texts.craftIcebreakerPlaceholder || 'Craft your personalized icebreaker here...'"
                :disabled="selectedLead.icebreaker_status === 'sent' || selectedLead.icebreaker_status === 'replied'"
              ></textarea>
              <div class="d-flex justify-content-between align-items-center">
                <button @click="getAISuggestion" class="btn btn-sm btn-outline-secondary" :disabled="isAISuggesting">
                  <i class="bi bi-magic"></i>
                  <span v-if="isAISuggesting" class="spinner-border spinner-border-sm ms-1" role="status" aria-hidden="true"></span>
                  {{ texts.getAISuggestion || 'AI Suggestion' }}
                </button>
                <button
                  @click="sendIcebreaker(selectedLead)"
                  class="btn btn-sm btn-primary"
                  :disabled="!currentIcebreakerMessage.trim() || selectedLead.icebreaker_status === 'sent' || selectedLead.icebreaker_status === 'replied' || isSendingIcebreaker"
                >
                 <span v-if="isSendingIcebreaker" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                  <i class="bi bi-send"></i> {{ texts.sendIcebreakerButton || 'Send Icebreaker' }}
                </button>
              </div>
              <small v-if="selectedLead.icebreaker_sent_at" class="text-muted d-block mt-2">
                {{ texts.sentOn || 'Sent:' }} {{ formatDate(selectedLead.icebreaker_sent_at) }}
              </small>
            </div>
          </div>

          <!-- Follow-up & Activity Log Section -->
          <div class="card mb-3">
            <div class="card-header">{{ texts.activityAndFollowUpsTitle || 'Activity & Follow-ups' }}</div>
            <div class="card-body">
              <!-- Form to Add New Follow-up/Log Interaction -->
              <div class="mb-3 p-2 border rounded">
                <h6 class="small">{{ texts.logOrSchedule || 'Log Interaction / Schedule Follow-up' }}</h6>
                <select class="form-select form-select-sm mb-2" v-model="newActivityType">
                  <option value="log_email_reply">{{ texts.logEmailReply || 'Log Email Reply' }}</option>
                  <option value="log_call">{{ texts.logCall || 'Log Call' }}</option>
                  <option value="log_meeting">{{ texts.logMeeting || 'Log Meeting' }}</option>
                  <option value="schedule_follow_up">{{ texts.scheduleFollowUpEmail || 'Schedule Follow-up Email' }}</option>
                  <option value="schedule_follow_up_call">{{ texts.scheduleFollowUpCall || 'Schedule Follow-up Call' }}</option>
                </select>
                <textarea class="form-control form-control-sm mb-2" rows="2" v-model="newActivityNotes" :placeholder="texts.notesPlaceholder || 'Notes...'"></textarea>
                <input v-if="newActivityType.startsWith('schedule_')" type="datetime-local" class="form-control form-control-sm mb-2" v-model="newActivityDateTime">
                <button @click="logOrScheduleActivity(selectedLead)" class="btn btn-sm btn-outline-primary w-100">{{ texts.addActivityButton || 'Add Activity' }}</button>
              </div>

              <!-- Activity Log -->
              <h6 class="small mt-3">{{ texts.historyLog || 'History:'}}</h6>
              <ul v-if="selectedLead.activity_log && selectedLead.activity_log.length > 0" class="list-unstyled activity-log-list">
                <li v-for="activity in selectedLead.activity_log" :key="activity.id" class="mb-2 small p-2 border-bottom">
                  <strong>{{ getActivityTypeDisplay(activity.type) }}:</strong> {{ activity.notes }}
                  <br><small class="text-muted">{{ formatDate(activity.timestamp) }}</small>
                  <span v-if="activity.follow_up_due_date" class="ms-2 badge bg-info text-dark">{{ texts.followUpDue || 'Follow-up Due:' }} {{ formatDate(activity.follow_up_due_date) }}</span>
                </li>
              </ul>
              <p v-else class="small text-muted">{{ texts.noActivityYet || 'No activity logged yet.'}}</p>
            </div>
          </div>

           <!-- Notes Section (General Notes for this lead in the hub) -->
          <div class="card">
            <div class="card-header">{{ texts.generalNotesTitle || 'General Notes' }}</div>
            <div class="card-body">
              <textarea class="form-control" rows="3" v-model="selectedLeadNotes" :placeholder="texts.addNotesPlaceholder || 'Add notes specific to your engagement...'"></textarea>
              <button @click="saveLeadNotes(selectedLead)" class="btn btn-sm btn-outline-secondary mt-2">{{ texts.saveNotesButton || 'Save Notes' }}</button>
            </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useLanguageStore } from '@/stores/languageStore';
// import { useEngagementStore } from '@/stores/engagementStore'; // Hypothetical store for this view's data

// Define types (consider moving to a dedicated types file if they grow)
interface EngagementLead {
  id: string;
  user_id: string; // From original Lead
  // Copied from Lead object when added to hub
  first_name?: string | null;
  last_name?: string | null;
  name?: string | null; // Could be a computed from first/last
  job_title?: string | null;
  company_name?: string | null;
  linkedIn_url?: string | null;
  email?: string | null; // Crucial for sending icebreakers

  // Engagement-specific fields
  icebreaker_message?: string | null;
  icebreaker_status: 'not_sent' | 'sent' | 'opened' | 'replied' | 'bounced' | 'error';
  icebreaker_status_display?: string; // For internationalized status
  icebreaker_sent_at?: string | null; // ISO Date string
  last_interaction_at?: string | null; // ISO Date string
  next_follow_up_date?: string | null; // ISO Date string
  next_follow_up_task?: string | null;
  engagement_notes?: string | null;
  activity_log?: EngagementActivity[];
  // avatar_url?: string | null; // if you have avatars
}

interface EngagementActivity {
  id: string; // uuid
  type: 'icebreaker_sent' | 'email_reply_received' | 'call_logged' | 'meeting_logged' | 'follow_up_scheduled_email' | 'follow_up_scheduled_call' | 'note_added';
  notes: string;
  timestamp: string; // ISO Date string
  follow_up_due_date?: string | null; // ISO Date string for scheduled follow-ups
}


const languageStore = useLanguageStore();
// const engagementStore = useEngagementStore(); // To fetch/update leads in the hub

const texts = computed(() => languageStore.texts); // Assuming texts are loaded in languageStore

const searchQuery = ref('');
const filterStatus = ref('');
const leadsInHub = ref<EngagementLead[]>([]); // This would come from your store/backend
const selectedLead = ref<EngagementLead | null>(null);
const isLoading = ref(false);
const isAISuggesting = ref(false);
const isSendingIcebreaker = ref(false);

const currentIcebreakerMessage = ref('');
const selectedLeadNotes = ref('');

// For new activity/follow-up form
const newActivityType = ref<'log_email_reply' | 'log_call' | 'log_meeting' | 'schedule_follow_up' | 'schedule_follow_up_call'>('log_email_reply');
const newActivityNotes = ref('');
const newActivityDateTime = ref('');


// Dummy data for example
// onMounted(async () => {
//   isLoading.value = true;
//   // Replace with actual fetch from engagementStore or Supabase table for engagement leads
//   await new Promise(resolve => setTimeout(resolve, 1000));
//   leadsInHub.value = [
//     { id: 'lead1', user_id: 'user1', name: 'Alice Wonderland', job_title: 'Dreamer', company_name: 'Curious Inc.', email: 'alice@example.com', icebreaker_status: 'not_sent', icebreaker_status_display: 'To Send' },
//     { id: 'lead2', user_id: 'user1', name: 'Bob The Builder', job_title: 'Constructor', company_name: 'BuildIt Co.', email: 'bob@example.com', icebreaker_status: 'sent', icebreaker_sent_at: new Date().toISOString(), icebreaker_status_display: 'Sent', next_follow_up_date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString() },
//     { id: 'lead3', user_id: 'user1', name: 'Charlie Brown', job_title: 'Philosopher', company_name: 'Peanuts LLC', email: 'charlie@example.com', icebreaker_status: 'replied', icebreaker_status_display: 'Replied' },
//   ];
//   isLoading.value = false;
// });


const filteredLeads = computed(() => {
  return leadsInHub.value.filter(lead => {
    const matchesSearch = (
      lead.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      lead.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      lead.job_title?.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
    const matchesStatus = filterStatus.value ? lead.icebreaker_status === filterStatus.value : true;
    // Add more complex filtering (e.g. follow_up_due)
    return matchesSearch && matchesStatus;
  }).sort((a,b) => (a.name || '').localeCompare(b.name || '')); // Simple sort
});

watch(selectedLead, (newLead) => {
  if (newLead) {
    currentIcebreakerMessage.value = newLead.icebreaker_message || '';
    selectedLeadNotes.value = newLead.engagement_notes || '';
    // Reset new activity form
    newActivityType.value = 'log_email_reply';
    newActivityNotes.value = '';
    newActivityDateTime.value = '';
  } else {
    currentIcebreakerMessage.value = '';
    selectedLeadNotes.value = '';
  }
});

function selectLead(lead: EngagementLead) {
  selectedLead.value = lead;
}

function formatDate(dateString?: string | null) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function getStatusDisplay(status: EngagementLead['icebreaker_status']): string {
  // This should ideally come from texts for i18n
  switch (status) {
    case 'not_sent': return texts.value.statusNotSent || 'To Send';
    case 'sent': return texts.value.statusSent || 'Sent';
    case 'opened': return texts.value.statusOpened || 'Opened';
    case 'replied': return texts.value.statusRepliedEngagement || 'Replied'; // Ensure unique key if different from filter
    case 'bounced': return texts.value.statusBounced || 'Bounced';
    case 'error': return texts.value.statusError || 'Error';
    default: return status;
  }
}
function getIcebreakerStatusClass(status: EngagementLead['icebreaker_status']): string {
  switch (status) {
    case 'not_sent': return 'secondary';
    case 'sent': return 'info';
    case 'opened': return 'primary';
    case 'replied': return 'success';
    case 'bounced':
    case 'error': return 'danger';
    default: return 'light';
  }
}
function getActivityTypeDisplay(type: EngagementActivity['type']): string {
  // This should come from texts.value
  return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}


async function getAISuggestion() {
  if (!selectedLead.value) return;
  isAISuggesting.value = true;
  // TODO: Implement API call to your AI service
  // const suggestion = await MyAIService.getIcebreaker(selectedLead.value);
  await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API call
  currentIcebreakerMessage.value = `Hi ${selectedLead.value.first_name || selectedLead.value.name}, noticed your work at ${selectedLead.value.company_name} in ${selectedLead.value.job_title}. Would love to connect! (AI Generated)`;
  isAISuggesting.value = false;
}

async function sendIcebreaker(lead: EngagementLead) {
  if (!lead || !lead.email || !currentIcebreakerMessage.value.trim()) return;
  isSendingIcebreaker.value = true;
  // TODO: Implement actual email sending logic (e.g., via Supabase Edge Function or backend)
  // await engagementStore.sendIcebreaker(lead.id, currentIcebreakerMessage.value);
  console.log(`Sending to ${lead.email}: ${currentIcebreakerMessage.value}`);
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call

  // Update lead status locally (and then persist via store/API)
  const leadInHub = leadsInHub.value.find(l => l.id === lead.id);
  if (leadInHub) {
    leadInHub.icebreaker_status = 'sent';
    leadInHub.icebreaker_sent_at = new Date().toISOString();
    leadInHub.icebreaker_message = currentIcebreakerMessage.value; // Save the sent message
    // Add to activity log
    if (!leadInHub.activity_log) leadInHub.activity_log = [];
    leadInHub.activity_log.unshift({
      id: crypto.randomUUID(), // or uuidv4() if imported
      type: 'icebreaker_sent',
      notes: `Icebreaker: "${currentIcebreakerMessage.value.substring(0,50)}..."`,
      timestamp: new Date().toISOString()
    });
  }
  isSendingIcebreaker.value = false;
}

async function logOrScheduleActivity(lead: EngagementLead) {
  if (!lead || !newActivityNotes.value.trim()) return;
  // TODO: Persist this to your backend/Supabase
  // await engagementStore.logActivity(lead.id, newActivityType.value, newActivityNotes.value, newActivityDateTime.value || undefined);
  console.log('Logging/Scheduling:', newActivityType.value, newActivityNotes.value, newActivityDateTime.value);

  const leadInHub = leadsInHub.value.find(l => l.id === lead.id);
  if (leadInHub) {
    if (!leadInHub.activity_log) leadInHub.activity_log = [];
    const activity: EngagementActivity = {
      id: crypto.randomUUID(),
      type: newActivityType.value as EngagementActivity['type'], // Cast needed if newActivityType is broader
      notes: newActivityNotes.value,
      timestamp: new Date().toISOString(),
    };
    if (newActivityType.value.startsWith('schedule_') && newActivityDateTime.value) {
      activity.follow_up_due_date = new Date(newActivityDateTime.value).toISOString();
      leadInHub.next_follow_up_date = activity.follow_up_due_date; // Update quick view
      // Potentially update leadInHub.next_follow_up_task here
    }
    if (newActivityType.value === 'log_email_reply') {
        leadInHub.icebreaker_status = 'replied'; // Update icebreaker status on reply
    }
    leadInHub.activity_log.unshift(activity);
    leadInHub.last_interaction_at = activity.timestamp;

    // Reset form
    newActivityNotes.value = '';
    newActivityDateTime.value = '';
    newActivityType.value = 'log_email_reply';
  }
}
async function saveLeadNotes(lead: EngagementLead) {
  if (!lead) return;
  // TODO: Persist selectedLeadNotes.value to your backend/Supabase for lead.id
  // await engagementStore.updateNotes(lead.id, selectedLeadNotes.value);
  console.log(`Saving notes for ${lead.id}: ${selectedLeadNotes.value}`);
   const leadInHub = leadsInHub.value.find(l => l.id === lead.id);
   if(leadInHub) leadInHub.engagement_notes = selectedLeadNotes.value;

  // You might want a visual confirmation
}

async function removeFromHub(lead: EngagementLead) {
  if (!confirm(`Are you sure you want to remove ${lead.name} from the Engagement Hub? This won't delete the lead itself.`)) return;
  // TODO: Call store/API to remove this lead from the engagement hub (e.g., update a flag or delete from engagement table)
  // await engagementStore.removeFromHub(lead.id);
  leadsInHub.value = leadsInHub.value.filter(l => l.id !== lead.id);
  if (selectedLead.value && selectedLead.value.id === lead.id) {
    selectedLead.value = null;
  }
}

// TODO: onMounted - fetch leads for this hub from a dedicated Supabase table or based on a flag on the main 'leads' table.
// TODO: Add methods to add leads from the 'new'/'saved' tabs to this engagement center.
//       This usually involves:
//       1. In LeadGenFormView: A button/action "Add to Engagement Hub".
//       2. This action calls a Supabase function or direct insert to:
//          a. Create a new record in an 'engagement_leads' table with a foreign key to the original lead.
//          b. OR, set a flag like 'in_engagement_hub = true' on the existing 'leads' record.
//       3. The EngagementCenterView then fetches leads where this condition is met.

</script>

<style scoped>
.engagement-center-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%; /* Assumes parent provides height, like .app-main-content-area */
  overflow: hidden;
  background-color: var(--content-bg-current);
}

.view-header {
  flex-shrink: 0;
  /* background-color: var(--card-bg-current); Use a slightly different bg if needed */
}
.view-header h3 {
    color: var(--text-color-base-current);
}

.engagement-main-content {
  display: flex;
  flex-grow: 1;
  overflow: hidden; /* Important for children to scroll independently */
  min-height: 0; /* Fix for flex children scrolling in Firefox/Safari */
}

.lead-queue-sidebar {
  width: 300px; /* Adjust as needed */
  min-width: 240px;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  background-color: var(--card-bg-current);
  flex-shrink: 0;
}

.selected-lead-workspace {
  flex-grow: 1;
  /* background-color: var(--content-bg-current); */ /* Or a slightly different shade like --bs-gray-100 */
}

.scrollable-area {
  overflow-y: auto;
}

.lead-list-items .list-group-item {
  cursor: pointer;
  padding: 0.75rem 1rem;
}
.lead-list-items .list-group-item.active {
  background-color: var(--primary-color-current);
  border-color: var(--primary-color-current);
  color: #fff; /* Ensure text is white on primary background */
}
.lead-list-items .list-group-item.active .text-muted {
  color: rgba(255,255,255,0.75) !important;
}
.lead-list-items .list-group-item.active .text-primary {
  color: rgba(255,255,255,0.85) !important; /* Slightly lighter for primary text on primary bg */
}


.lead-details-and-actions .card {
    border-color: var(--border-color-current);
}
.lead-details-and-actions .card-header {
    background-color: var(--card-bg-light); /* Lighter header for cards within */
    border-bottom: 1px solid var(--border-color-current);
    font-weight: 500;
    padding: 0.75rem 1rem;
}
html[data-bs-theme="dark"] .lead-details-and-actions .card-header {
    background-color: color-mix(in srgb, var(--card-bg-current) 90%, #fff 5%);
}


.activity-log-list li {
  font-size: 0.85rem;
}
.activity-log-list li strong {
  color: var(--text-color-base-current);
}

/* Consider specific badge colors for different icebreaker statuses */
.badge.bg-secondary { /* For 'not_sent' */
    background-color: var(--bs-gray-500) !important;
}
.badge.bg-info { /* For 'sent' */
    background-color: var(--bs-info) !important;
}
.badge.bg-primary { /* For 'opened' */
    background-color: var(--bs-blue) !important;
}
.badge.bg-success { /* For 'replied' */
    background-color: var(--bs-success) !important;
}
.badge.bg-danger { /* For 'bounced', 'error' */
    background-color: var(--bs-danger) !important;
}

</style>