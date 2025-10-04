# 🧪 Productivity Hub - Testing Guide

Complete testing checklist for all features and functionalities.

## 🎯 Pre-Testing Setup

### 1. Fresh Installation Test
```bash
# Delete existing database
rm productivity.db

# Start application
python app.py
```

### 2. Database Initialization
- ✅ Application starts without errors
- ✅ Database file `productivity.db` is created
- ✅ All tables are created (tasks, habits, user_settings)

## 📊 Dashboard Testing

### Initial State
- [ ] Productivity Score shows 0
- [ ] Tasks Completed shows 0/0
- [ ] Total Streak Days shows 0
- [ ] Active Habits shows 0
- [ ] All stat cards display with correct colors
- [ ] All icons display correctly (🏆, 🎯, 🔥, 📈)

### After Adding Data
- [ ] Productivity Score updates in real-time
- [ ] Task completion counter increments
- [ ] Streak days reflect habit streaks
- [ ] Active habits count matches number of habits

### Score Calculation Test
1. Add and complete 2 tasks (should show 20 points)
2. Add habit and mark done for 3 days (should add 15 points)
3. Verify: Score = (2 × 10) + (3 × 5) = 35

## ✅ Task Management Testing

### Adding Tasks
- [ ] Empty task input doesn't create task
- [ ] Valid task appears in list immediately
- [ ] Task input clears after adding
- [ ] Tasks appear in descending order (newest first)
- [ ] Enter key submits task

### Task Display
- [ ] Task shows with unchecked checkbox
- [ ] Task title displays correctly
- [ ] Delete button appears on hover
- [ ] Task item has smooth hover effect

### Completing Tasks
- [ ] Clicking checkbox marks task complete
- [ ] Task text gets strike-through styling
- [ ] Task text becomes gray/faded
- [ ] Celebration modal appears
- [ ] Dashboard updates immediately
- [ ] Checkbox shows checked state

### Uncompleting Tasks
- [ ] Unchecking checkbox removes completion
- [ ] Strike-through removed
- [ ] Task returns to normal styling
- [ ] Dashboard updates (score decreases)

### Deleting Tasks
- [ ] Confirmation dialog appears
- [ ] Task removed from list on confirm
- [ ] Cancel keeps task in place
- [ ] Dashboard updates after deletion

### Edge Cases
- [ ] Very long task names wrap properly
- [ ] Special characters in task names work
- [ ] Multiple rapid task additions work
- [ ] Task list scrolls when many tasks added

## 🔥 Habit Tracking Testing

### Adding Habits
- [ ] Empty habit input doesn't create habit
- [ ] Valid habit appears in list immediately
- [ ] Habit input clears after adding
- [ ] Habits appear in descending order (newest first)
- [ ] Enter key submits habit

### Habit Display
- [ ] Habit name displays correctly
- [ ] Streak badge shows with 0 initially
- [ ] Progress bar shows at 0%
- [ ] "Mark Done" button is active
- [ ] Delete button appears on hover
- [ ] Fire emoji (🔥) displays in streak badge

### Marking Habit Done
**Day 1:**
- [ ] Click "Mark Done" button
- [ ] Button changes to "✓ Done Today!"
- [ ] Button becomes disabled (green background)
- [ ] Streak increases to 1
- [ ] Progress bar increases
- [ ] Celebration modal shows "1 Day Streak!"
- [ ] Dashboard updates

**Day 2 (same day):**
- [ ] Button stays disabled
- [ ] Cannot mark done again same day
- [ ] Streak stays at 1

**Day 3 (next day - manual test):**
- [ ] Change system date or wait 24 hours
- [ ] Button becomes active again
- [ ] Marking done increases streak to 2
- [ ] Celebration shows "2 Day Streak!"

### Streak Reset Testing
**Manual Test (requires waiting or date manipulation):**
- [ ] Build 3-day streak
- [ ] Skip one day (don't mark done)
- [ ] Next day, streak resets to 1 when marked
- [ ] Background scheduler resets streak at midnight

### Progress Bar
- [ ] 0 streak = 0% progress
- [ ] 15 days = 50% progress
- [ ] 30 days = 100% progress
- [ ] Bar animates smoothly

### Deleting Habits
- [ ] Confirmation dialog appears
- [ ] Habit removed from list on confirm
- [ ] Cancel keeps habit in place
- [ ] Dashboard updates after deletion

### Edge Cases
- [ ] Very long habit names wrap properly
- [ ] Multiple habits track independently
- [ ] Rapid marking/unmarking works
- [ ] Habit list scrolls when many habits added

## 🎉 Celebration Modal Testing

### Trigger Conditions
- [ ] Appears on task completion
- [ ] Appears on habit marking
- [ ] Shows correct message for tasks
- [ ] Shows streak count for habits

### Modal Behavior
- [ ] Centered on screen
- [ ] Dark overlay behind modal
- [ ] Emoji displays (🎉)
- [ ] Custom text shows correctly
- [ ] "Continue" button works
- [ ] Modal closes on button click
- [ ] Can't interact with page while modal open
- [ ] Smooth fade-in animation

### Messages
**Task completion:**
- Text: "Task Completed! 🎉"
- Subtext: "You're on fire! Keep it up!"

**Habit streaks:**
- Text: "[X] Day Streak! 🔥"
- Subtext: "Amazing consistency! Keep building that habit!"

## 🔄 Real-time Updates Testing

### Dashboard Auto-refresh
- [ ] Dashboard stats update on task actions
- [ ] Dashboard stats update on habit actions
- [ ] Stats refresh every 30 seconds
- [ ] No page reload required

### List Updates
- [ ] Task list refreshes after add/delete
- [ ] Habit list refreshes after add/delete
- [ ] Animations play on new items
- [ ] No duplicate entries appear

## 🎨 UI/UX Testing

### Responsive Design
**Desktop (1920px):**
- [ ] 4 stat cards in one row
- [ ] Tasks and habits side by side
- [ ] All content visible

**Tablet (768px):**
- [ ] Stat cards stack appropriately
- [ ] Tasks and habits remain readable
- [ ] No horizontal scroll

**Mobile (375px):**
- [ ] All cards stack vertically
- [ ] Touch targets are large enough
- [ ] Text remains readable
- [ ] No content cutoff

### Visual Effects
- [ ] Hover effects on all cards
- [ ] Button hover state changes
- [ ] Smooth transitions (0.2-0.3s)
- [ ] Delete buttons fade in on hover
- [ ] Progress bars animate smoothly
- [ ] Task strike-through animates

### Color Scheme
- [ ] Purple cards: Productivity score
- [ ] Green cards: Tasks completed
- [ ] Orange/yellow cards: Streak days
- [ ] Blue cards: Active habits
- [ ] Consistent brand colors throughout

### Typography
- [ ] Headers are bold and readable
- [ ] Body text has good contrast
- [ ] Icon sizes are consistent
- [ ] No text overflow

## 🔧 Backend API Testing

### Using Browser Developer Tools or Postman

**GET /api/dashboard**
```bash
curl http://localhost:5000/api/dashboard
```
- [ ] Returns JSON with all stats
- [ ] Status code 200

**POST /api/tasks**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task"}'
```
- [ ] Creates task
- [ ] Returns task object
- [ ] Status code 201

**PUT /api/tasks/1**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
```
- [ ] Updates task
- [ ] Returns updated task
- [ ] Status code 200

**DELETE /api/tasks/1**
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```
- [ ] Deletes task
- [ ] Status code 200

**POST /api/habits**
```bash
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Habit"}'
```
- [ ] Creates habit
- [ ] Returns habit object
- [ ] Status code 201

**PUT /api/habits/1**
```bash
curl -X PUT http://localhost:5000/api/habits/1 \
  -H "Content-Type: application/json" \
  -d '{"mark_done":true}'
```
- [ ] Updates habit streak
- [ ] Returns updated habit
- [ ] Status code 200

## 🛡️ Error Handling Testing

### Invalid Inputs
- [ ] Empty task title rejected
- [ ] Empty habit name rejected
- [ ] Invalid dates handled gracefully
- [ ] Malformed JSON returns 400

### Database Errors
- [ ] Non-existent ID returns 404
- [ ] Database connection issues handled
- [ ] Concurrent requests don't corrupt data

### Browser Console
- [ ] No JavaScript errors
- [ ] No 404 errors for resources
- [ ] AJAX requests complete successfully
- [ ] Proper error messages logged

## ⏰ Background Scheduler Testing

### Streak Reset Functionality
**Test Setup:**
1. Create habit and mark done
2. Build 3-day streak
3. Don't mark done for 2 days

**Expected Behavior:**
- [ ] Scheduler runs at midnight (00:01)
- [ ] Streak resets to 0 after skip
- [ ] `done_today` flag resets daily
- [ ] No errors in console

**Manual Test:**
```python
# In Python console
from app import app, check_and_reset_streaks
with app.app_context():
    check_and_reset_streaks()
```

## 📱 Cross-Browser Testing

### Chrome
- [ ] All features work
- [ ] UI renders correctly
- [ ] Animations smooth

### Firefox
- [ ] All features work
- [ ] UI renders correctly
- [ ] Animations smooth

### Safari
- [ ] All features work
- [ ] UI renders correctly
- [ ] Animations smooth

### Edge
- [ ] All features work
- [ ] UI renders correctly
- [ ] Animations smooth

## 🚀 Performance Testing

### Load Time
- [ ] Initial page load < 2 seconds
- [ ] Dashboard data loads < 500ms
- [ ] Task list loads < 300ms
- [ ] Habit list loads < 300ms

### Scalability
**Test with 50 tasks:**
- [ ] List renders quickly
- [ ] No lag when scrolling
- [ ] Actions remain responsive

**Test with 20 habits:**
- [ ] All progress bars render
- [ ] No performance degradation
- [ ] Updates remain fast

## ✅ Final Checklist

### Core Functionality
- [ ] All CRUD operations work for tasks
- [ ] All CRUD operations work for habits
- [ ] Streak logic functions correctly
- [ ] Dashboard calculates score accurately
- [ ] Background scheduler runs properly

### User Experience
- [ ] UI matches design mockup
- [ ] All animations smooth
- [ ] No visual bugs
- [ ] Responsive on all devices
- [ ] Intuitive user flow

### Code Quality
- [ ] No console errors
- [ ] No broken links
- [ ] Proper error handling
- [ ] Clean code structure
- [ ] Comments where needed

## 🐛 Known Issues / Future Fixes

Document any bugs found during testing:

1. Issue: _______________
   - Steps to reproduce: _______________
   - Expected: _______________
   - Actual: _______________
   - Priority: High/Medium/Low

---

**Testing completed by:** _______________  
**Date:** _______________  
**Version:** 1.0.0